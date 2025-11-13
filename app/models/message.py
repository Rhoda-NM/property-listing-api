from datetime import datetime
from ..extensions import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.receiver_id} regarding Listing {self.listing_id}>'