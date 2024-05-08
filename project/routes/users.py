from datetime import datetime, timedelta

import jwt
from flask import request, url_for, render_template, current_app, redirect
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_mail import Message
from flask_restx import Namespace, Resource, abort
from jwt import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash

from project.extensions import db, mail
from project.schemas.authorization import authorizations
from project.schemas.service_info import service_info_for_teacher
from project.schemas.users import (
    user_model,
    user_login_parser,
    user_login_response,
    user_register_parser,
    user_change_password_parser,
    email_schema,
    password_schema,
    expert_register_parser,
    teacher_register_parser,
)
from project.models import User, Teacher, Role, Roles, Specialist, Position, University

user_ns = Namespace(
    name="user", description="User related endpoints", authorizations=authorizations
)


def create_expert(args):
    """create new expert in database"""
    email = args.get("email")

    if Specialist.query.filter_by(email=email).first():
        abort(400, f"Expert with email '{email}' already exists")

    name = " ".join(
        [
            args.get("first_name"),
            args.get("parent_name") or "",
            args.get("last_name"),
        ]
    ).replace("  ", " ")

    expert = Specialist(
        company=args.get("company"),
        name=name,
        position=args.get("position"),
        email=args.get("email"),
        phone=args.get("phone") or "",
        professional_field=args.get("professional_field"),
        discipline_type=args.get("discipline_type"),
        experience=args.get("experience"),
        url_cv=args.get("url_cv") or "",
        role_id=Role.query.filter_by(name=Roles.SPECIALIST).first().id,
    )

    return expert


def create_teacher(args):
    """create new teacher in database"""
    email = args.get("email")

    if Teacher.query.filter_by(email=email).first():
        return None

    name = " ".join(
        [
            args.get("first_name"),
            args.get("parent_name") or "",
            args.get("last_name"),
        ]
    ).replace("  ", " ")

    teacher = Teacher(
        name=name,
        position_id=args.get("position_id"),
        email=args.get("email"),
        department_id=args.get("department_id"),
        comments=args.get("comments") or "",
        degree_level=args.get("degree_level") or "",
        role_id=Role.query.filter_by(name=Roles.TEACHER).first().id,
    )

    return teacher


def create_user(args, role: Roles):
    """create new user in database and send email with confirmation token"""

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
        role_id=Role.query.filter_by(name=role).first().id,
    )

    return user


class SecurityUtils:
    @staticmethod
    def encrypt_data(data):
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        data_with_exp = {**data, "exp": expiration_time}
        encrypted_token = jwt.encode(
            data_with_exp,
            current_app.config["JWT_SECRET_KEY"],
            algorithm=current_app.config["JWT_ALGORITHM"],
        )
        return encrypted_token

    @staticmethod
    def decrypt_data(data):
        decrypted_data = jwt.decode(
            data,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGORITHM"]],
        )
        return decrypted_data

    @staticmethod
    def send_confirm_token(user, front_url):
        token = SecurityUtils.encrypt_data(
            {"email": user.email, "front_url": front_url}
        )
        url_confirm = url_for("user_confirm_mail", token=token, _external=True)
        confirm_mail = render_template(
            "confirm_email.html", confirm_url=url_confirm, user=user
        )
        SecurityUtils.send_mail(
            user, subject="Education UA - Confirm email", template=confirm_mail
        )

    @staticmethod
    def send_mail(user, subject, template):
        msg = Message(
            subject=subject,
            recipients=[user.email],
            html=template,
        )
        mail.send(msg)


@user_ns.route("/register/user")
class RegisterUser(Resource):

    @user_ns.expect(user_register_parser)
    @user_ns.marshal_with(user_model)
    def post(self):
        """Register new user"""
        args = user_register_parser.parse_args()
        user = create_user(args, Roles.USER)

        SecurityUtils.send_confirm_token(user, request.headers.get("Origin"))

        db.session.add(user)
        db.session.commit()

        return user, 201


@user_ns.route("/register/expert")
class RegisterExpert(Resource):

    @user_ns.expect(expert_register_parser)
    @user_ns.marshal_with(user_model)
    def post(self):
        """Register new expert"""
        args = expert_register_parser.parse_args()
        user_expert = create_user(args, Roles.SPECIALIST)
        expert = create_expert(args)

        SecurityUtils.send_confirm_token(user_expert, request.headers.get("Origin"))

        db.session.add(user_expert)
        db.session.add(expert)
        db.session.commit()

        return user_expert, 201


@user_ns.route("/register/teacher")
class RegisterTeacher(Resource):

    @user_ns.marshal_with(service_info_for_teacher, envelope="service_info")
    def get(self):
        """Service info for registering a teacher"""
        positions = Position.query.all()
        university = University.query.all()
        return {"position": positions, "university": university}

    @user_ns.expect(teacher_register_parser)
    @user_ns.marshal_with(user_model)
    def post(self):
        """Register new teacher"""
        args = teacher_register_parser.parse_args()
        user_teacher = create_user(args, Roles.TEACHER)
        teacher = create_teacher(args)

        SecurityUtils.send_confirm_token(user_teacher, request.headers.get("Origin"))

        db.session.add(user_teacher)
        if teacher:
            db.session.add(teacher)
        db.session.commit()

        return user_teacher, 201


@user_ns.route("/login")
class Login(Resource):

    @user_ns.response(
        401,
        "One of: \n"
        "'User with email <email> does not exist'\n"
        "'Incorrect password'\n"
        "'Email <email> is not confirmed. Please check your email'\n"
        "'User with email <email> is banned'",
    )
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
        if not user.email_confirmed:
            abort(401, f"Email '{email}' is not confirmed. Please check your email")
        if not user.active_status:
            abort(401, f"User with email '{email}' is banned")

        user_role = user.role.name

        response = {
            "access_token": "Bearer "
            + create_access_token(
                identity=email,
                additional_claims={"role": user_role, "tokenType": "access"},
            ),
            "refresh_token": "Bearer "
            + create_refresh_token(
                identity=email,
                additional_claims={"role": user_role, "tokenType": "refresh"},
            ),
            "role": user_role,
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "parent_name": user.parent_name,
            "email": user.email,
            "phone": user.phone,
            "verified": user.email_confirmed,
        }

        if user_role == Roles.TEACHER:
            teacher = Teacher.query.filter_by(email=email).first()
            response["id"] = teacher.id
            response["verified"] = teacher.verified
        elif user_role == Roles.SPECIALIST:
            expert = Specialist.query.filter_by(email=email).first()
            response["id"] = expert.id
            response["verified"] = expert.verified

        return response


@user_ns.route("/confirm_mail/<string:token>")
class ConfirmMail(Resource):
    @user_ns.doc(description="Confirm Mail")
    def get(self, token: str):

        try:
            decrypted_data = SecurityUtils.decrypt_data(token)
        except ExpiredSignatureError:
            return abort(401, "The link has expired")

        email = decrypted_data.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            return abort(404, f"User with {email} is not registered")

        user.email_confirmed = True
        db.session.commit()

        front_url = decrypted_data.get("front_url")
        if front_url:
            return redirect(front_url + "/auth")

        return "Success confirm mail", 201


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
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        user_role = user.role.name
        response = {
            "access_token": "Bearer "
            + create_access_token(
                identity=email,
                additional_claims={"role": user_role, "tokenType": "access"},
            ),
            "refresh_token": "Bearer "
            + create_refresh_token(
                identity=email,
                additional_claims={"role": user_role, "tokenType": "refresh"},
            ),
            "role": user_role,
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "parent_name": user.parent_name,
            "email": user.email,
            "phone": user.phone,
            "verified": user.email_confirmed,
        }

        if user_role == Roles.TEACHER:
            teacher = Teacher.query.filter_by(email=email).first()
            response["id"] = teacher.id
            response["verified"] = teacher.verified
        elif user_role == Roles.SPECIALIST:
            expert = Specialist.query.filter_by(email=email).first()
            response["id"] = expert.id
            response["verified"] = expert.verified

        return response


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
