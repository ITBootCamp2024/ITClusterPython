from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)
from flask_restx import Namespace, Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db
from project.schemas.users import (
    user_model,
    user_login_parser,
    user_login_response,
    user_register_parser, user_change_password_parser)
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

        user_role = user.role.name

        if user_role == "user":
            if Teacher.query.filter_by(email=email).first():
                user.role = Role.query.filter_by(name="teacher").first()
                db.session.commit()
                user_role = "teacher"

            # TODO: add check for user role if it's email is in specialist table

        claims = {"role": user_role}
        return {
            "access_token": create_access_token(identity=user.email, additional_claims=claims),
            "refresh_token": create_refresh_token(identity=user.email, additional_claims=claims),
            "role": user_role,
        }


@user_ns.route("/refresh")
class Refresh(Resource):
    @user_ns.doc(security="jsonWebToken")
    @user_ns.doc(description="Refresh the access and refresh tokens (refresh token is required)")
    @jwt_required(refresh=True)
    @user_ns.marshal_with(user_login_response)
    def post(self):
        identity = get_jwt_identity()
        user_role = get_jwt().get("role")
        claims = {"role": user_role}
        return {
            "access_token": create_access_token(identity=identity, additional_claims=claims),
            "refresh_token": create_refresh_token(identity=identity, additional_claims=claims),
            "role": user_role,
        }


@user_ns.route("/change-password")
class ChangePassword(Resource):
    @user_ns.doc(security="jsonWebToken",
                 description="Change the password of the current user",
                 responses={200: "Password changed"})
    @jwt_required()
    @user_ns.expect(user_change_password_parser)
    def post(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user:
            abort(401, f"User with email '{email}' does not exist")

        args = user_change_password_parser.parse_args()
        old_password = args.get("old_password")

        if not check_password_hash(user.password_hash, old_password):
            abort(401, "Incorrect old password")

        new_password = args.get("new_password")
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return {"message": "Password changed"}, 200
