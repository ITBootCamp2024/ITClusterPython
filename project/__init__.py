from datetime import timedelta
from os import environ

from dotenv import load_dotenv
from flask import Flask, g, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.extensions import api, db, migrate, pagination, jwt, mail
from project.models import (
    Department,
    Discipline,
    DisciplineBlock,
    DisciplineGroup,
    EducationLevel,
    EducationProgram,
    Position,
    Specialty,
    Teacher,
    University,
)
from project.routes.courses import courses_ns
from project.routes.departments import departments_ns
from project.routes.disciplines import disciplines_ns
from project.routes.discipline_blocks import discipline_blocks_ns
from project.routes.discipline_groups import discipline_groups_ns
from project.routes.education_levels import education_levels_ns
from project.routes.education_programs import education_programs_ns
from project.routes.position import position_ns
from project.routes.service_info import service_info_ns
from project.routes.specialty import specialty_ns
from project.routes.teachers import teachers_ns
from project.routes.test_roles import test_roles_ns
from project.routes.universities import university_ns

from project.routes.test_jwt_education_levels import education_levels_ns as test_jwt
from project.routes.users import user_ns


def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 1
    app.config["RESTX_VALIDATE"] = True
    app.config["RESTX_JSON"] = {"ensure_ascii": False}
    app.config["DEBUG"] = True

    # Possible configurations for Paginate
    # app.config['PAGINATE_PAGE_SIZE'] = 20
    # app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
    # app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
    # app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
    app.config["PAGINATE_PAGINATION_OBJECT_KEY"] = None
    app.config["PAGINATE_DATA_OBJECT_KEY"] = "content"
    app.config["JSON_AS_ASCII"] = False

    # TODO згенерувати JWT_SECRET_KEY для прода. інструкція у пайтон консоль:
    #  import secrets
    #  print(secrets.token_hex(16))
    app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
    app.config["JWT_ALGORITHM"] = environ.get("JWT_ALGORITHM")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = environ.get("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    pagination.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    @app.teardown_appcontext
    def close_connection(exception=None):
        try:
            db.session.remove()
        except SQLAlchemyError as e:
            print(f"An error occurred while closing the database connection: {str(e)}")

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        if hasattr(g, "db"):
            g.db.rollback()
            g.db.session.close()
        return (
            jsonify(
                {
                    "message": "can't write data to the database",
                    "error": f"Integrity error occurred. {error}",
                }
            ),
            400,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        if hasattr(g, "db"):
            g.db.rollback()
            g.db.session.close()
        return (
            jsonify(
                {
                    "message": "Database error occured",
                    "error": f"Database error occurred. {error}",
                }
            ),
            500,
        )

    api.add_namespace(courses_ns)
    api.add_namespace(departments_ns)
    api.add_namespace(disciplines_ns)
    api.add_namespace(discipline_blocks_ns)
    api.add_namespace(discipline_groups_ns)
    api.add_namespace(education_levels_ns)
    api.add_namespace(education_programs_ns)
    api.add_namespace(position_ns)
    api.add_namespace(service_info_ns)
    api.add_namespace(specialty_ns)
    api.add_namespace(teachers_ns)
    api.add_namespace(university_ns)
    api.add_namespace(user_ns)
    api.add_namespace(test_roles_ns)
    # TODO цей неймспейс для тесту JWT, потім його видалити і його ендпойнти і сам модуль test_jwt_education_levels
    api.add_namespace(test_jwt)

    # @jwt.user_identity_loader
    # def user_identity_lookup(user):
    #     return user.id  # probably we will use email as identifier
    #
    # @jwt.user_lookup_loader
    # def user_lookup_callback(_jwt_header, jwt_data):
    #     identity = jwt_data["sub"]
    #     return User.query.filter_by(id=identity).first()

    return app
