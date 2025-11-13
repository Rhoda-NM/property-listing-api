from datetime import datetime, date

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.booking import Booking
from ..models.listing import Listing
from ..models.user import User
from ..schemas.booking import BookingSchema

bookings_ns = Namespace("bookings", description="Bookings & viewing requests")

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)


def current_user():
    uid = get_jwt_identity()
    return User.query.get(uid) if uid else None


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def ranges_overlap(a_start: date, a_end: date, b_start: date, b_end: date) -> bool:
    """Return True if two inclusive ranges [a_start, a_end] and [b_start, b_end] overlap."""
    return not (a_end < b_start or b_end < a_start)


# Swagger models
booking_in = bookings_ns.model("BookingIn", {
    "listing_id": fields.Integer(required=True, description="ID of the listing to book"),
    "guest_name": fields.String(required=True),
    "guest_email": fields.String,
    "start_date": fields.String(required=True, description="Start date (YYYY-MM-DD)"),
    "end_date": fields.String(required=True, description="End date (YYYY-MM-DD)"),
})

booking_status_update = bookings_ns.model("BookingStatusUpdate", {
    "status": fields.String(required=True, description="New status (pending/confirmed/cancelled)"),
})


@bookings_ns.route("")
class BookingList(Resource):
    @bookings_ns.expect(booking_in, validate=True)
    @bookings_ns.response(201, "Booking created")
    @bookings_ns.response(400, "Validation error")
    @bookings_ns.response(404, "Listing not found")
    def post(self):
        """Create a booking request for a listing (public)"""
        data = request.get_json() or {}

        listing = Listing.query.get(data["listing_id"])
        if not listing:
            return {"message": "Listing not found"}, 404

        try:
            start = parse_date(data["start_date"])
            end = parse_date(data["end_date"])
        except ValueError:
            return {"message": "Dates must be in YYYY-MM-DD format"}, 400

        if end < start:
            return {"message": "end_date cannot be before start_date"}, 400

        # Check for overlap with existing bookings for this listing
        existing = Booking.query.filter(
            Booking.listing_id == listing.id,
            Booking.status.in_(["pending", "confirmed"]),
        ).all()

        for b in existing:
            if ranges_overlap(start, end, b.start_date, b.end_date):
                return {
                    "message": "Dates not available for this listing",
                    "conflict": booking_schema.dump(b),
                }, 400

        booking = Booking(
            listing_id=listing.id,
            guest_name=data["guest_name"],
            guest_email=data.get("guest_email"),
            start_date=start,
            end_date=end,
            status="pending",
        )
        db.session.add(booking)
        db.session.commit()

        return booking_schema.dump(booking), 201

    @jwt_required()
    @bookings_ns.doc(params={
        "status": "Filter by status (pending/confirmed/cancelled)",
        "page": "Page number (default 1)",
        "per_page": "Items per page (default 20, max 100)",
    })
    @bookings_ns.response(200, "Bookings fetched")
    @bookings_ns.response(403, "Agents only")
    def get(self):
        """List bookings for the current agent's listings"""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Agents only"}, 403

        args = request.args
        page = int(args.get("page", 1))
        per_page = min(int(args.get("per_page", 20)), 100)
        status = args.get("status")

        # bookings joined to listings, filtered by agent
        q = (
            db.session.query(Booking)
            .join(Listing, Booking.listing_id == Listing.id)
            .filter(Listing.agent_id == user.id)
            .order_by(Booking.start_date.desc())
        )
        if status:
            q = q.filter(Booking.status == status)

        paged = q.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": bookings_schema.dump(paged.items),
            "total": paged.total,
            "page": page,
            "per_page": per_page,
        }


@bookings_ns.route("/<int:booking_id>")
class BookingDetail(Resource):
    @jwt_required()
    @bookings_ns.response(200, "Booking fetched")
    @bookings_ns.response(403, "Forbidden")
    @bookings_ns.response(404, "Booking not found")
    def get(self, booking_id: int):
        """Get a booking (only owning agent can view)"""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Agents only"}, 403

        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        listing = Listing.query.get(booking.listing_id)
        if not listing or listing.agent_id != user.id:
            return {"message": "Forbidden"}, 403

        return booking_schema.dump(booking)

    @jwt_required()
    @bookings_ns.expect(booking_status_update, validate=True)
    @bookings_ns.response(200, "Booking updated")
    @bookings_ns.response(403, "Forbidden")
    @bookings_ns.response(404, "Booking not found")
    def patch(self, booking_id: int):
        """Update booking status (owning agent only)"""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Agents only"}, 403

        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        listing = Listing.query.get(booking.listing_id)
        if not listing or listing.agent_id != user.id:
            return {"message": "Forbidden"}, 403

        data = request.get_json() or {}
        new_status = data.get("status")
        if new_status not in ["pending", "confirmed", "cancelled"]:
            return {"message": "Invalid status"}, 400

        booking.status = new_status
        db.session.commit()

        return booking_schema.dump(booking)
