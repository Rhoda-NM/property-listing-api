from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..extensions import db
from ..models.user import User
from ..schemas.user import UserSchema

auth_ns = Namespace('Auth', description='Authentication operations')    
user_schema = UserSchema()

#swagger models
register_model = auth_ns.model("Register", {
    "name": fields.String(required=True, example="Agent Alice"),
    "email": fields.String(required=True, example="alice.agent@example.com"),
    "password": fields.String(required=True, example="password123"),
    "phone": fields.String(example="+254700000001"),
    "is_agent": fields.Boolean(default=False, example=True),
    "bio": fields.String(example="Specialist in apartments around Nairobi."),
    "company": fields.String(example="Nairobi Homes Ltd"),
})

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True, example="alice.agent@example.com"),
    "password": fields.String(required=True, example="password123"),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Validation Error')
    def post(self):
        """Register a new user"""
        data = request.get_json() or {}
        if not data.get("email") or not data.get("password") or not data.get("name"):
            return {"message": "name, email, password required"}, 400
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already registered"}, 400
        user = User(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        password_hash=generate_password_hash(data["password"]),
        is_agent=bool(data.get("is_agent", False)),
        bio=data.get("bio"),
        company=data.get("company"),
        )
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        return {"access_token": token, "user": user_schema.dump(user)}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Logi and return access token"""
        data = request.get_json() or {}
        user = User.query.filter_by(email=data.get("email")).first()
        if not user or not check_password_hash(user.password_hash, data.get("password", "")):
            return {"message": "Invalid credentials"}, 401
        token = create_access_token(identity=user.id)
        return {"access_token": token, "user": user_schema.dump(user)}

