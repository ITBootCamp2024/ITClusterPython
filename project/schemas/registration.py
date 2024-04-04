from flask_restx import fields
from marshmallow import validate
from project.extensions import api

user_registration_schema = api.model(
    "UserRegistration",
    {
        "first_name": fields.String(
            required=True,
            description="The first name of the user",
            min_length=2,
            max_length=50
        ),
        "last_name": fields.String(
            required=True,
            description="The last name of the user",
            min_length=2,
            max_length=50
        ),
        "middle_name": fields.String(
            description="The middle name of the user",
            max_length=50
        ),
        "email": fields.String(
            required=True,
            description="The email of the user",
            validate=validate.Email()
        ),
        "phone_number": fields.String(
            description="The phone number of the user",
            min_length=10,
            max_length=20,

        ),
        "password": fields.String(
            required=True,
            description="The password of the user",
            min_length=6
        ),
        "confirm_password": fields.String(
           required=True,
           description="The password confirmation of the user",
           min_length=6
        )
    }
)


user_schema = {
    "id": fields.Integer(description="The user unique identifier"),
    "first_name": fields.String(description="The first name of the user"),
    "last_name": fields.String(description="The last name of the user"),
    "middle_name": fields.String(description="The middle name of the user"),
    "email": fields.String(description="The email of the user"),
    "phone_number": fields.String(description="The phone number of the user"),
}