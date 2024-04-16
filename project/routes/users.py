from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Namespace, Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db
from project.schemas.users import (
    user_model,
    user_login_parser,
    user_login_response,
    user_register_parser)
from project.models import User, Teacher, Role

user_ns = Namespace(name="user", description="User related endpoints")


@user_ns.route("/register")
class Register(Resource):

    @user_ns.expect(user_register_parser)
    @user_ns.marshal_with(user_model)
    def post(self):
        args = user_register_parser.parse_args()
        email = args.get("email")

        if User.query.filter_by(email=email).first():
            abort(400, f"User with email '{email}' already exists")

        user = User(
            email=email,
            password_hash=generate_password_hash(args.get("password")),
            first_name=args.get("first_name"),
            last_name=args.get("last_name"),
            parent_name=args.get("parent_name") or "",
            phone=args.get("phone") or "",
            role_id=Role.query.filter_by(name="user").first().id,
        )
        db.session.add(user)
        db.session.commit()
        return user, 201


@user_ns.route("/login")
class Login(Resource):

    @user_ns.expect(user_login_parser)
    @user_ns.marshal_with(user_login_response)
    def post(self):
        args = user_login_parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(401, f"User with email '{email}' does not exist")
        if not check_password_hash(user.password_hash, password):
            abort(401, "Incorrect password")

        # TODO: uncomment checking for the email being confirmed
        # if not user.email_confirmed:
        #     abort(401, f"Email '{email}' is not confirmed. Please check your email.")

        if user.role.name == "user":
            if Teacher.query.filter_by(email=email).first():
                user.role = Role.query.filter_by(name="teacher").first()
                db.session.commit()

            # TODO: add check for user role if it's email is in specialist table

        return {
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
            "role": user.role.name,
        }
