from datetime import datetime
from ..extensions import db


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)
    property_type = db.Column(db.String(50), default='apartment')
    status = db.Column(db.String(20), default='active')
    address = db.Column(db.String(200))
    city = db.Column(db.String(120))
    lat = db.Column(db.Float, index=True)
    lng = db.Column(db.Float, index=True)
    image_urls = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Listing {self.title} - {self.city}>'