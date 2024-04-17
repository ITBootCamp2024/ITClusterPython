from os import environ

import jwt
from dotenv import load_dotenv

from flask import request, url_for, render_template
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_mail import Message
from flask_restx import Namespace, Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db, mail
from project.schemas.users import (
    user_model,
    user_login_parser,
    user_login_response,
    user_register_parser,
)
from project.models import User, Teacher, Role

user_ns = Namespace(name="user", description="User related endpoints")

load_dotenv()
KEY = environ.get("JWT_SECRET_KEY")
ALGORITHM = environ.get("JWT_ALGORITHM")


class SecurityUtils:
    @staticmethod
    def encrypt_data(data):
        encrypted_token = jwt.encode(data, KEY, algorithm=ALGORITHM)
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
        # TODO: Add an email template.
        msg = Message(
            subject=subject,
            sender=environ.get("EMAIL_USER"),
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


@user_ns.route("/confirm_mail/<string:token>")
class ConfirmMail(Resource):
    def get(self, token: str):
        decrypted_data = SecurityUtils.decrypt_data(token)
        user = User.query.filter_by(email=decrypted_data["email"]).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            return "Success confirm mail"
        return "Link not valid"


@user_ns.route("/reset_password/")
class ResetPassword(Resource):

    def post(self):
        data = request.json
        email = data.get("email")
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                data_to_encrypt = {"user_id": user.id, "email": user.email}
                encrypted_data = SecurityUtils.encrypt_data(data_to_encrypt)
                link = url_for("user_reset_password", token=encrypted_data, _external=True)
                subject_mail = "It Cluster - Reset Password"
                confirm_mail = render_template(
                    "reset_password.html", confirm_url=link, user=user
                )
                SecurityUtils.send_mail(
                    user, subject=subject_mail, template=confirm_mail
                )
                return link

            return abort(401, f"User with email '{email}' does not exist")

        return abort(401, f"Send your mail")


@user_ns.route("/reset_password/<string:token>")
class ResetPasswordPatch(Resource):

    @staticmethod
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
