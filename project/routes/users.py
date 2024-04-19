from datetime import datetime, timedelta
from os import environ

import jwt
from dotenv import load_dotenv

from flask import request, url_for, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_mail import Message
from flask_restx import Namespace, Resource, abort
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db, mail
from project.schemas.users import (
    user_model,
    user_login_parser,
    user_login_response,
    user_register_parser,
    user_change_password_parser,
    email_schema,
    password_schema,
)
from project.models import User, Teacher, Role

user_ns = Namespace(name="user", description="User related endpoints")

load_dotenv()
KEY = environ.get("JWT_SECRET_KEY")
ALGORITHM = environ.get("JWT_ALGORITHM")


class SecurityUtils:
    @staticmethod
    def encrypt_data(data):
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        data_with_exp = {**data, "exp": expiration_time}
        encrypted_token = jwt.encode(data_with_exp, KEY, algorithm=ALGORITHM)
        return encrypted_token

    @staticmethod
    def decrypt_data(data):
        decrypted_data = jwt.decode(
            data,
            KEY,
            algorithms=[ALGORITHM],
        )
        return decrypted_data

    @staticmethod
    def send_mail(user, subject, template):
        msg = Message(
            subject=subject,
            sender=environ.get("MAIL_USERNAME"),
            recipients=[user.email],
            html=template,
        )
        mail.send(msg)


@user_ns.route("/register")
class Register(Resource):

    @staticmethod
    def send_confirm_token(user):
        token = SecurityUtils.encrypt_data({"email": user.email})
        url_confirm = url_for("user_confirm_mail", token=token, _external=True)
        confirm_mail = render_template(
            "confirm_email.html", confirm_url=url_confirm, user=user
        )
        SecurityUtils.send_mail(
            user, subject="It Cluster - Confirm mail", template=confirm_mail
        )

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

        self.send_confirm_token(user)
        return user, 201


@user_ns.route("/login")
class Login(Resource):

    @user_ns.expect(user_login_parser)
    @user_ns.marshal_with(user_login_response)
    def post(self):
        args = user_login_parser.parse_args()
        email = args.get("email")
        password = args.get("password")
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
            "access_token": create_access_token(
                identity=user.email, additional_claims=claims
            ),
            "refresh_token": create_refresh_token(
                identity=user.email, additional_claims=claims
            ),
            "role": user_role,
        }


@user_ns.route("/confirm_mail/<string:token>")
class ConfirmMail(Resource):
    @user_ns.doc(
        description="Confirm Mail",
        responses={
            201: "Success confirm mail",
            401: "The link has expired",
            404: "Link not valid",
        },
    )
    def get(self, token: str):

        try:
            decrypted_data = SecurityUtils.decrypt_data(token)
        except ExpiredSignatureError:
            return "The link has expired", 401

        email = decrypted_data["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            return "Success confirm mail", 201
        return f"User with {email} is not registered", 404


@user_ns.route("/reset_password/")
class ResetPassword(Resource):

    @user_ns.doc(
        description="When client recover your password, an email is sent with the link",
        responses={
            201: "The email was sent successfully",
            401: "Send correct mail",
            404: "User with email '{email}' does not exist",
        },
    )
    @user_ns.expect(email_schema)
    def post(self):
        data = request.json

        email = data.get("email")
        if not email:
            abort(401, "Send correct mail")

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, f"User with email '{email}' does not exist")

        data_to_encrypt = {"user_id": user.id, "email": user.email}
        encrypted_data = SecurityUtils.encrypt_data(data_to_encrypt)
        link = url_for("user_reset_password", token=encrypted_data, _external=True)
        subject_mail = "It Cluster - Reset Password"
        confirm_mail = render_template("reset_password.html", url=link, user=user)
        SecurityUtils.send_mail(user, subject=subject_mail, template=confirm_mail)
        return {"message": "The email was sent successfully"}, 201


@user_ns.route("/reset_password/<string:token>")
class ResetPasswordPatch(Resource):

    @staticmethod
    @user_ns.doc(
        description="When a token and password are transferred, the password of the user with this token is changed.",
        responses={201: "Done", 404: "Password or user not found"},
    )
    @user_ns.expect(password_schema)
    def patch(token: str):
        data = request.json
        decrypted_data = SecurityUtils.decrypt_data(token)
        user_id, email = decrypted_data.values()
        user = User.query.filter_by(email=email).first()
        password = data.get("password")
        if user and password:
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            return "Done", 201
        return {"message": "Password or user not found"}, 404


@user_ns.route("/refresh")
class Refresh(Resource):
    @user_ns.doc(security="jsonWebToken")
    @user_ns.doc(
        description="Refresh the access and refresh tokens (refresh token is required)"
    )
    @jwt_required(refresh=True)
    @user_ns.marshal_with(user_login_response)
    def post(self):
        identity = get_jwt_identity()
        user_role = get_jwt().get("role")
        claims = {"role": user_role}
        return {
            "access_token": create_access_token(
                identity=identity, additional_claims=claims
            ),
            "refresh_token": create_refresh_token(
                identity=identity, additional_claims=claims
            ),
            "role": user_role,
        }


@user_ns.route("/change-password")
class ChangePassword(Resource):
    @user_ns.doc(
        security="jsonWebToken",
        description="Change the password of the current user",
        responses={200: "Password changed"},
    )
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
