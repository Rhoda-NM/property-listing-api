from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()      # <-- real Marshmallow extension (has init_app)
migrate = Migrate()
jwt = JWTManager()

# Global error handler for Marshmallow validation errors