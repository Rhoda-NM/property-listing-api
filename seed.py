from datetime import date

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import User, Listing, Message, Booking


def seed():
    app = create_app()
    with app.app_context():
        print("Seeding database...")

        # Clear tables (optional – comment out if you don't want this)
        db.drop_all()
        db.create_all()

        # ---- Users ----
        agent1 = User(
            name="Agent Alice",
            email="alice.agent@example.com",
            phone="+254700000001",
            password_hash=generate_password_hash("password123"),
            is_agent=True,
            bio="Specialist in apartments around Nairobi.",
            company="Nairobi Homes Ltd",
        )

        agent2 = User(
            name="Agent Brian",
            email="brian.agent@example.com",
            phone="+254700000002",
            password_hash=generate_password_hash("password123"),
            is_agent=True,
            bio="Coastal properties and holiday homes.",
            company="Coastal Realty",
        )

        user1 = User(
            name="Regular User",
            email="user@example.com",
            phone="+254700000003",
            password_hash=generate_password_hash("password123"),
            is_agent=False,
            bio="Looking for a nice 2BR to rent.",
        )

        db.session.add_all([agent1, agent2, user1])
        db.session.commit()

        # ---- Listings ----
        l1 = Listing(
            title="Modern 2BR Apartment in Kilimani",
            description="Spacious 2BR with balcony, close to Yaya Centre.",
            price=80000,
            bedrooms=2,
            bathrooms=2,
            property_type="apartment",
            status="active",
            address="Argwings Kodhek Road",
            city="Nairobi",
            lat=-1.2921,
            lng=36.7831,
            agent_id=agent1.id,
        )

        l2 = Listing(
            title="3BR Townhouse in Karen",
            description="Quiet gated community with garden.",
            price=150000,
            bedrooms=3,
            bathrooms=3,
            property_type="townhouse",
            status="active",
            address="Karen Plains",
            city="Nairobi",
            lat=-1.3370,
            lng=36.7200,
            agent_id=agent1.id,
        )

        l3 = Listing(
            title="Beachfront 2BR in Nyali",
            description="Ocean view, fully furnished, great for holidays.",
            price=120000,
            bedrooms=2,
            bathrooms=2,
            property_type="apartment",
            status="active",
            address="Nyali Beach Road",
            city="Mombasa",
            lat=-4.0333,
            lng=39.6833,
            agent_id=agent2.id,
        )

        db.session.add_all([l1, l2, l3])
        db.session.commit()

        # ---- Messages ----
        m1 = Message(
            listing_id=l1.id,
            name="Prospect One",
            email="prospect1@example.com",
            phone="+254700123456",
            content="Hi, is this 2BR in Kilimani still available?",
        )

        m2 = Message(
            listing_id=l3.id,
            name="Holiday Guest",
            email="holiday@example.com",
            phone="+254700654321",
            content="Can I book the Nyali apartment for Christmas week?",
        )

        db.session.add_all([m1, m2])
        db.session.commit()

        # ---- Bookings ----
        b1 = Booking(
            listing_id=l3.id,
            guest_name="Holiday Guest",
            guest_email="holiday@example.com",
            start_date=date(2025, 12, 20),
            end_date=date(2025, 12, 27),
            status="confirmed",
        )

        b2 = Booking(
            listing_id=l2.id,
            guest_name="Viewing Client",
            guest_email="client@example.com",
            start_date=date(2025, 11, 25),
            end_date=date(2025, 11, 25),
            status="pending",
        )

        db.session.add_all([b1, b2])
        db.session.commit()

        print("✅ Seeding complete.")


if __name__ == "__main__":
    seed()
