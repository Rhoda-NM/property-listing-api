from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.message import Message
from ..models.listing import Listing
from ..models.user import User
from ..schemas.message import MessageSchema

messages_ns = Namespace("messages", description="Listing inquiries and messages")

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

# Swagger model for incoming message
message_in = messages_ns.model("MessageIn", {
    "listing_id": fields.Integer(required=True, description="ID of the listing"),
    "name": fields.String(required=True, description="Name of the person sending the message"),
    "email": fields.String(description="Email of the person sending the message"),
    "phone": fields.String(description="Phone number of the person sending the message"),
    "content": fields.String(required=True, description="Message content"),
})


def current_user():
    uid = get_jwt_identity()
    return User.query.get(uid) if uid else None


@messages_ns.route("")
class MessageList(Resource):
    @messages_ns.expect(message_in, validate=True)
    @messages_ns.response(201, "Message created")
    @messages_ns.response(404, "Listing not found")
    def post(self):
        """Send a message about a listing (public endpoint)"""
        data = request.get_json() or {}

        listing = Listing.query.get(data["listing_id"])
        if not listing:
            return {"message": "Listing not found"}, 404

        msg = Message(
            listing_id=listing.id,
            name=data["name"],
            email=data.get("email"),
            phone=data.get("phone"),
            content=data["content"],
        )
        db.session.add(msg)
        db.session.commit()

        return message_schema.dump(msg), 201

    @jwt_required()
    @messages_ns.doc(params={
        "page": "Page number (default 1)",
        "per_page": "Items per page (default 20, max 100)",
    })
    @messages_ns.response(200, "Messages fetched")
    @messages_ns.response(403, "Agents only")
    def get(self):
        """List messages for the current agent's listings"""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Agents only"}, 403

        args = request.args
        page = int(args.get("page", 1))
        per_page = min(int(args.get("per_page", 20)), 100)

        # join Message -> Listing to filter by agent
        q = (
            db.session.query(Message)
            .join(Listing, Message.listing_id == Listing.id)
            .filter(Listing.agent_id == user.id)
            .order_by(Message.created_at.desc())
        )

        paged = q.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": messages_schema.dump(paged.items),
            "total": paged.total,
            "page": page,
            "per_page": per_page,
        }


@messages_ns.route("/<int:message_id>")
class MessageDetail(Resource):
    @jwt_required()
    @messages_ns.response(200, "Message fetched")
    @messages_ns.response(403, "Forbidden")
    @messages_ns.response(404, "Message not found")
    def get(self, message_id: int):
        """Get a single message (only the listing's agent can view)"""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Agents only"}, 403

        msg = Message.query.get(message_id)
        if not msg:
            return {"message": "Message not found"}, 404

        listing = Listing.query.get(msg.listing_id)
        if not listing or listing.agent_id != user.id:
            return {"message": "Forbidden"}, 403

        return message_schema.dump(msg)
