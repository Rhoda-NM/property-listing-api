from datetime import datetime
from ..extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_email = db.Column(db.String(120))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id} for Listing {self.listing_id} by User {self.user_id}>'