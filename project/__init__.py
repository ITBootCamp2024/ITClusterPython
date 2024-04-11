from os import environ

from dotenv import load_dotenv
from flask import Flask, g, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from project.extensions import api, db, migrate, pagination
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
from project.routes.universities import university_ns


def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://Python_healththee:7bb73aee46fd73bd7cd9377a2be48e436e419712@cqa.h.filess.io:3307/Python_healththee"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["RESTX_VALIDATE"] = True
    app.config["RESTX_JSON"] = {"ensure_ascii": False}
    app.config['DEBUG'] = True

    # Possible configurations for Paginate
    # app.config['PAGINATE_PAGE_SIZE'] = 20
    # app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
    # app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
    # app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
    app.config["PAGINATE_PAGINATION_OBJECT_KEY"] = None
    app.config['PAGINATE_DATA_OBJECT_KEY'] = "content"
    app.config['JSON_AS_ASCII'] = False

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    pagination.init_app(app, db)

    @app.before_request
    def before_request():
        g.db = db.session

    @app.after_request
    def after_request(response):
        db_session = getattr(g, "db", None)
        if db_session is not None:
            db_session.close()
        return response

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        if hasattr(g, "db"):
            g.db.rollback()
        return jsonify({"error": f"Integrity error occurred. {error}"}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        if hasattr(g, "db"):
            g.db.rollback()
        return jsonify({"error": f"Database error occurred. {error}"}), 500

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
    return app
