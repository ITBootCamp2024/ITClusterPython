from flask_restx import fields, reqparse

from project.extensions import api

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

email_parser = reqparse.RequestParser()
email_parser.add_argument("email", type=str, required=True, location="form")

user_login_parser = email_parser.copy()
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
        "role": fields.String(description="Role", required=True, default="role"),
        "id": fields.Integer(description="Teacher or expert id"),
        "verified": fields.Boolean(description="Whether teacher or expert is verified"),
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "parent_name": fields.String(description="Parent name"),
        "email": fields.String(description="Email"),
        "phone": fields.String(description="Phone"),
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

teacher_register_request_model = api.model(
    "TeacherRegisterRequestModel",
    {
        "name": fields.String(description="Teacher's name", required=True),
        "university": fields.String(description="university", required=True),
        "department": fields.String(description="department", required=True),
        "email": fields.String(description="email", required=True),
    }
)

user_change_password_parser = reqparse.RequestParser()
user_change_password_parser.add_argument("old_password", type=str, required=True, location="form")
user_change_password_parser.add_argument("new_password", type=str, required=True, location="form")

token_parser = reqparse.RequestParser()
token_parser.add_argument("token", type=str, required=True)