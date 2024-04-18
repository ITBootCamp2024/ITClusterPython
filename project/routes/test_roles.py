from flask import jsonify
from flask_jwt_extended import get_jwt
from flask_restx import Resource, Namespace

from project.schemas.authorization import authorizations
from project.validators import allowed_roles


test_roles_ns = Namespace(name="test-roles", description="Test roles", authorizations=authorizations)


@test_roles_ns.route("/admin-only")
class AdminOnly(Resource):
    @allowed_roles(["admin"])
    @test_roles_ns.doc(security="jsonWebToken")
    @test_roles_ns.doc(description="Admin only endpoint")
    def get(self):
        return jsonify({
            "message": "You have access because you are admin",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/teacher-only")
class TeacherOnly(Resource):
    @allowed_roles(["teacher"])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify({
            "message": "You have access because you are teacher",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/user-only")
class UserOnly(Resource):
    @allowed_roles(["user"])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify({
            "message": "You have access because you are user",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/admin-and-teacher")
class AdminAndTeacher(Resource):
    @test_roles_ns.doc(security="jsonWebToken")
    @allowed_roles(["admin", "teacher"])
    def get(self):
        return jsonify({
            "message": "You have access because you are admin or teacher",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/admin-and-user")
class AdminAndUser(Resource):
    @allowed_roles(["admin", "user"])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify({
            "message": "You have access because you are admin or user",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/teacher-and-user")
class TeacherAndUser(Resource):
    @allowed_roles(["teacher", "user"])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify({
            "message": "You have access because you are teacher or user",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/admin-and-teacher-and-user")
class AdminAndTeacherAndUser(Resource):
    @allowed_roles(["admin", "teacher", "user"])
    @test_roles_ns.doc(security="jsonWebToken")
    def get(self):
        return jsonify({
            "message": "You have access because you are admin, teacher or user",
            "role": get_jwt().get("role")
        })


@test_roles_ns.route("/jwt-token-is-optional")
class JwtTokenIsOptional(Resource):
    @allowed_roles(["admin", "teacher", "user"], optional=True)
    def get(self):
        return jsonify({
            "message": "Everyone has access. Even without a token",
            "role": get_jwt().get("role")
        })
