from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Namespace, Resource
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db
from project.schemas.user import user_model, login_model, register_model
from project.models import User


user_ns = Namespace(name="user")


@user_ns.route("/register")
class Register(Resource):

    @user_ns.expect(register_model)
    @user_ns.marshal_with(user_model)
    def post(self):
        user = User(
            email=user_ns.payload["email"],
            password_hash=generate_password_hash(user_ns.payload["password"]),
            first_name=user_ns.payload["first_name"],
            last_name=user_ns.payload["last_name"],
            parent_name=user_ns.payload["parent_name"],
            phone=user_ns.payload["phone"],

        )
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
        return {"access_token": create_access_token(user.email),
                "refresh_token": create_refresh_token(user.email)}
