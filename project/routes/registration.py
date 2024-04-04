from flask import request, jsonify
from flask_restx import Resource, Namespace
from project.extensions import db, api
from project.models import User
from flask_bcrypt import generate_password_hash
from project.schemas.registration import user_registration_schema, user_schema

user = Namespace(name="signup", description="User registration")


@user.route("", methods=["POST"])
class UserRegistration(Resource):
    @user.expect(user_registration_schema)
    def post(self):
        data = request.json
        if data["password"] != data["confirm_password"]:
            return {"message": "Password and confirm password do not match"}, 400

        hashed_password = generate_password_hash(data["password"]).decode('utf-8')
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data.get("middle_name", ""),
            email=data["email"],
            phone_number=data.get("phone_number", ""),
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return {"user": api.marshal(user, user_schema)}

