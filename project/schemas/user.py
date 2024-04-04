from flask_restx import fields

from project import api

login_model = api.model("LoginModel", {
    "email": fields.String,
    "password": fields.String
})

user_model = api.model("UserModel", {
    "id": fields.Integer,
    "email": fields.String
})
