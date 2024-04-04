from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from project import db
from project.models import User
from project.schemas.user import login_model, user_model

user_ns = Namespace(name="users", description="info about education programs")


@user_ns.route("/register")
class Register(Resource):

    @user_ns.expect(login_model)
    @user_ns.marshal_with(user_model)
    def post(self):
        user = User(email=user_ns.payload["email"], password_hash=generate_password_hash(user_ns.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201


@user_ns.route("/login")
class Login(Resource):

    @user_ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(email=user_ns.payload["email"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, user_ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        return {"access_token": create_access_token(user)}
