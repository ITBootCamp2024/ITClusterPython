from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt
from flask_restx import Resource, Namespace
import jwt

from project.models import Roles
from project.schemas.authorization import authorizations
from project.validators import allowed_roles


test_roles_ns = Namespace(
    name="test-roles", description="Test roles", authorizations=authorizations
)


@test_roles_ns.route("/admin-only")
class AdminOnly(Resource):
    @allowed_roles([Roles.ADMIN])
    @test_roles_ns.doc(security="jsonWebToken")
    @test_roles_ns.doc(description="Admin only endpoint")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are admin",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/teacher-only")
class TeacherOnly(Resource):
    @allowed_roles([Roles.TEACHER])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are teacher",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/user-only")
class UserOnly(Resource):
    @allowed_roles([Roles.USER])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are user",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/admin-and-teacher")
class AdminAndTeacher(Resource):
    @test_roles_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.TEACHER])
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are admin or teacher",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/admin-and-user")
class AdminAndUser(Resource):
    @allowed_roles([Roles.ADMIN, Roles.USER])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are admin or user",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/teacher-and-user")
class TeacherAndUser(Resource):
    @allowed_roles([Roles.TEACHER, Roles.USER])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are teacher or user",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/admin-and-teacher-and-user")
class AdminAndTeacherAndUser(Resource):
    @allowed_roles([Roles.ADMIN, Roles.TEACHER, Roles.USER])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify(
            {
                "message": "You have access because you are admin, teacher or user",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/jwt-token-is-optional")
class JwtTokenIsOptional(Resource):
    @allowed_roles([Roles.ADMIN, Roles.TEACHER, Roles.USER], optional=True)
    def get(self):
        return jsonify(
            {
                "message": "Everyone has access. Even without a token",
                "role": get_jwt().get("role"),
            }
        )


@test_roles_ns.route("/token-decoding")
class TokenFields(Resource):
    def get(self):
        KEY = current_app.config["JWT_SECRET_KEY"]
        ALGORITHM = current_app.config["JWT_ALGORITHM"]
        headers = request.headers
        token = headers.get("Authorization")
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        decrypted_data = jwt.decode(
            token,
            KEY,
            algorithms=[ALGORITHM],
        )
        return decrypted_data
