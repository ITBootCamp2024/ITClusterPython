from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for


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
            max_length=45,
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


# paginated_university_model = get_pagination_schema_for(university_model)
