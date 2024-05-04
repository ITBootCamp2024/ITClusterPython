from flask_restx import fields, reqparse

from project.extensions import api

login_model = api.model(
    "LoginModel",
    {
        "email": fields.String(
            required=True,
            description="Email",
            min_length=1,
            max_length=45,
            default="example@mail.com",
        ),
        "password": fields.String,
    },
)

register_model = api.model(
    "RegisterModel",
    {
        "email": fields.String(
            required=True,
            description="Email",
            min_length=1,
            max_length=100,
            default="example@mail.com",
        ),
        "password": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "parent_name": fields.String,
        "phone": fields.String,
    },
)

user_model = api.model(
    "UserModel",
    {
        "id": fields.Integer,
        "first_name": fields.String,
        "last_name": fields.String,
        "parent_name": fields.String,
        "email": fields.String,
        "phone": fields.String,
    },
)

user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument("email", type=str, required=True, location="form")
user_login_parser.add_argument("password", type=str, required=True, location="form")

user_login_response = api.model(
    "UserLoginResponse",
    {
        "access_token": fields.String(
            description="Access token", required=True, default="access_token"
        ),
        "refresh_token": fields.String(
            description="Refresh token", required=True, default="refresh_token"
        ),
        "role": fields.String(
            description="Role", required=True, default="role"
        ),
        "id": fields.Integer(
            description="Teacher or expert id"
        ),
        "verified": fields.Boolean(
            description="Whether teacher or expert is verified"
        ),
    },
)

user_register_parser = reqparse.RequestParser()
user_register_parser.add_argument("email", type=str, required=True, location="form")
user_register_parser.add_argument("password", type=str, required=True, location="form")
user_register_parser.add_argument("first_name", type=str, required=True, location="form")
user_register_parser.add_argument("last_name", type=str, required=True, location="form")
user_register_parser.add_argument("parent_name", type=str, required=False, location="form")
user_register_parser.add_argument("phone", type=str, required=False, location="form")

expert_register_parser = user_register_parser.copy()
expert_register_parser.add_argument("company", type=str, required=True, location="form")
expert_register_parser.add_argument("position", type=str, required=True, location="form")
expert_register_parser.add_argument("professional_field", type=str, required=True, location="form")
expert_register_parser.add_argument("discipline_type", type=str, required=True, location="form")
expert_register_parser.add_argument("experience", type=int, required=True, location="form")
expert_register_parser.add_argument("url_cv", type=str, required=False, location="form")

teacher_register_parser = user_register_parser.copy()
teacher_register_parser.add_argument("department_id", type=int, required=True, location="form")
teacher_register_parser.add_argument("position_id", type=int, required=True, location="form")
teacher_register_parser.add_argument("degree_level", type=str, required=False, location="form")
teacher_register_parser.add_argument("comments", type=str, required=False, location="form")

user_change_password_parser = reqparse.RequestParser()
user_change_password_parser.add_argument("old_password", type=str, required=True, location="form")
user_change_password_parser.add_argument("new_password", type=str, required=True, location="form")

email_schema = api.model(
    "Email",
    {"email": fields.String}
)

password_schema = api.model(
    "Password",
    {"password": fields.String}
)
