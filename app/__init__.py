import os
from flask import Flask, send_from_directory
from flask_restx import Api

from .config import Config
from .extensions import db, ma, migrate, jwt

# Global RESTX API instance (Swagger UI at /docs)
api = Api(
    title="Property Listing API",
    version="1.0",
    description="Listings • Agents • Geo Search • Messages • Bookings",
    doc="/docs",  # Swagger UI path
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Make sure upoad folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)


    # Extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Attach RESTX API to app
    api.init_app(app)

    # Import namespaces AFTER api.init_app
    from .resources.health import health_ns
    from .resources.auth import auth_ns
    from .resources.listings import listings_ns
    from .resources.agents import agents_ns
    from .resources.messages import messages_ns
    from .resources.bookings import bookings_ns

    # IMPORTANT: mount health at root, others at prefixes
    api.add_namespace(health_ns, path="/")            # /health
    api.add_namespace(auth_ns, path="/auth")          # /auth/...
    api.add_namespace(listings_ns, path="/listings")  # /listings/...
    api.add_namespace(agents_ns, path="/agents")   
    api.add_namespace(messages_ns, path="/messages")  # /agents/...
    api.add_namespace(bookings_ns, path="/bookings")  # /bookings/...
    
    # Server uploaded images (dev only)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Create DB (dev only)
    with app.app_context():
        db.create_all()

    return app
