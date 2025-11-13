import math
import os
import json
from uuid import uuid4

from flask import request, current_app
from flask_restx import Resource, Api, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from ..extensions import db
from ..models.listing import Listing
from ..models.user import User
from ..schemas.listing import ListingSchema


listings_ns = Namespace('Listings', description='Property listing operations')
listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Parser for file uploads (Swagger + request parsing)
upload_parser = listings_ns.parser()
upload_parser.add_argument(
    'images',
     location='files',
     type=FileStorage,
     required=True, 
     action="append",
     help='One or more image files',
)

def current_user():
    """Return the current logged-in user (or None)."""
    uid = get_jwt_identity()
    return User.query.get(uid) if uid else None

listing_in = listings_ns.model('ListingIn', {
    'title': fields.String(required=True, description='Title of the listing'),
    'description': fields.String(description='Description of the listing'),
    'price': fields.Float(required=True, description='Price of the listing'),
    'bedrooms': fields.Integer(description='Number of bedrooms'),
    'bathrooms': fields.Integer(description='Number of bathrooms'),
    'property_type': fields.String(description='Type of property'),
    'status': fields.String(description='Status of the listing'),
    'address': fields.String(description='Address of the property'),
    'city': fields.String(description='City where the property is located'),
    'lat': fields.Float(description='Latitude of the property location'),
    'lng': fields.Float(description='Longitude of the property location'),
})

R_EARTH_KM = 6371.0088

def haversine_km(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_EARTH_KM * c

@listings_ns.route('')
class ListingList(Resource):
    @listings_ns.doc(params={
        'city': 'Filter by city',
        'property_type': 'Filter by property type',
        'status': 'Filter by status',
        'min_price': 'Minimum price',
        'max_price': 'Maximum price',
        'bedrooms': 'Minimum number of bedrooms',
        'bathrooms': 'Minimum number of bathrooms',
        'page': 'Page number for pagination',
        'per_page': 'Number of items per page (max 100)',
    })
    def get(self):
        """List + filter listings."""
        q = Listing.query
        args = request.args

        if args.get("city"):
            q = q.filter(Listing.city.ilike(f"%{args['city']}%"))
        if args.get("property_type"):
            q = q.filter_by(property_type=args["property_type"])
        if args.get("status"):
            q = q.filter_by(status=args["status"])
        if args.get("min_price"):
            q = q.filter(Listing.price >= float(args["min_price"]))
        if args.get("max_price"):
            q = q.filter(Listing.price <= float(args["max_price"]))
        if args.get("bedrooms"):
            q = q.filter(Listing.bedrooms >= int(args["bedrooms"]))
        if args.get("bathrooms"):
            q = q.filter(Listing.bathrooms >= int(args["bathrooms"]))

        sort = args.get("sort", "-created_at")
        if sort.startswith("-"):
            q = q.order_by(getattr(Listing, sort[1:]).desc())
        else:
            q = q.order_by(getattr(Listing, sort).asc())

        page = int(args.get("page", 1))
        per_page = min(int(args.get("per_page", 20)), 100)
        paged = q.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": listings_schema.dump(paged.items),
            "total": paged.total,
            "page": page,
            "per_page": per_page,
        }

    @jwt_required()
    @listings_ns.expect(listing_in, validate=True)
    @listings_ns.response(201, 'Listing created successfully')
    @listings_ns.response(403, 'Only agents can create listings')
    def post(self):
        """Create a new listing (agents only)."""
        user = current_user()
        if not user or not user.is_agent:
            return {"message": "Only agents can create listings"}, 403

        data = request.get_json() or {}
        listing = Listing(
            agent_id=user.id,
            **{
                k: data.get(k)
                for k in [
                    "title",
                    "description",
                    "price",
                    "bedrooms",
                    "bathrooms",
                    "property_type",
                    "status",
                    "address",
                    "city",
                    "lat",
                    "lng",
                ]
            },
        )
        db.session.add(listing)
        db.session.commit()
        return listing_schema.dump(listing), 201

@listings_ns.route('/<int:listing_id>')
class ListingItem(Resource):
    def get(self, listing_id):
        """Get a single listing by ID."""
        listing = Listing.query.get_or_404(listing_id)
        return listing_schema.dump(listing)

    @jwt_required()
    def patch(self, listing_id):
        """Update a listing (only by owning agent)."""
        user = current_user()
        listing = Listing.query.get_or_404(listing_id)

        if not user or (not user.is_agent or listing.agent_id != user.id):
            return {"message": "Only the owning agent can update"}, 403

        data = request.get_json() or {}
        for k in [
            "title",
            "description",
            "price",
            "bedrooms",
            "bathrooms",
            "property_type",
            "status",
            "address",
            "city",
            "lat",
            "lng",
        ]:
            if k in data:
                setattr(listing, k, data[k])

        db.session.commit()
        return listing_schema.dump(listing)

    @jwt_required()
    def delete(self, listing_id):
        """Delete a listing (only by owning agent)."""
        user = current_user()
        listing = Listing.query.get_or_404(listing_id)

        if not user or (not user.is_agent or listing.agent_id != user.id):
            return {"message": "Only the owning agent can delete"}, 403

        db.session.delete(listing)
        db.session.commit()
        return {"message": "deleted"}

@listings_ns.route('/search')
class ListingGeoSearch(Resource):
    """
    GET /listings/search?lat=...&lng=...&radius_km=...
    - lat, lng: required
    - radius_km: optional, default 10 km
    """
    @listings_ns.doc(params={
        'lat': 'Latitude of the center point (required)',
        'lng': 'Longitude of the center point (required)',
        'radius_km': 'Search radius in kilometers (default 10 km)',
    })
    def get(self):
        """Geo-spatial search for listings within a radius."""
        args = request.args
        try:
            lat = float(args.get("lat"))
            lng = float(args.get("lng"))
        except (TypeError, ValueError):
            return {"message": "Query params 'lat' and 'lng' are required and must be numbers"}, 400

        try:
            radius_km = float(args.get("radius_km", 10))
        except ValueError:
            return {"message": "radius_km must be a number"}, 400

        listings = Listing.query.all()
        results = []

        for l in listings:
            if l.lat is None or l.lng is None:
                continue
            d = haversine_km(lat, lng, l.lat, l.lng)
            if d <= radius_km:
                item = listing_schema.dump(l)
                item["distance_km"] = round(d, 3)
                results.append(item)

        # sort by distance
        results.sort(key=lambda x: x["distance_km"])

        return {
            "items": results,
            "count": len(results),
            "lat": lat,
            "lng": lng,
            "radius_km": radius_km,
        }

@listings_ns.route('/<int:listing_id>/images')
class ListingImageUpload(Resource):
    @jwt_required()
    @listings_ns.expect(upload_parser)
    @listings_ns.response(200, 'Images uploaded successfully')
    @listings_ns.response(403, 'Only the owning agent can upload images')
    @listings_ns.response(400, 'Invalid file upload')
    def post(self, listing_id):
        """Upload images for a listing (only by owning agent)."""
        user = current_user()
        listing = Listing.query.get_or_404(listing_id)

        if not user or (not user.is_agent or listing.agent_id != user.id):
            return {"message": "Only the owning agent can upload images"}, 403

        args = upload_parser.parse_args()
        files = args.get('images')

        if not files:
            return {"message": "No images uploaded"}, 400

        upload_folder = current_app.config['UPLOAD_FOLDER']
        existing = json.loads(listing.image_urls or "[]")
        saved_urls = []

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                ext = filename.rsplit(".", 1)[1].lower()
                new_name = f"{uuid4().hex}.{ext}"
                filepath = os.path.join(upload_folder, new_name)
                f.save(filepath)
                saved_urls.append(f"/uploads/{new_name}")

        listing.image_urls = json.dumps(existing + saved_urls)
        db.session.commit()

        return {"image_urls": saved_urls}, 201
# 