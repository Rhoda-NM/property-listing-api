from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    password_hash = db.Column(db.String(255), nullable=False)
    is_agent = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)
    company = db.Column(db.String(120))
    
    listings = db.relationship('Listing', backref='agent', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'