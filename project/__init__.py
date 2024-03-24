from os import environ

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from project.extensions import api, db, migrate, pagination
from project.models import (
    ProgramLevel,
    Specialty,
    CourseBlocks,
    CourseStatuses,
    CourseGroupes,
    Teacher,
)
from project.routes.course_blocks import course_blocks_ns
from project.routes.course_groupes import course_groupes_ns
from project.routes.programs_levels import program_level_ns
from project.routes.specialty import specialty_ns
from project.routes.сourse_statuses import course_statuses_ns
from project.routes.teachers import teachers_ns
from project.routes.schools import school_ns
from project.routes.universities import university_ns


def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["RESTX_VALIDATE"] = True
    app.config["RESTX_JSON"] = {"ensure_ascii": False}

    # Possible configurations for Paginate
    # app.config['PAGINATE_PAGE_SIZE'] = 20
    # app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
    # app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
    # app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
    app.config["PAGINATE_PAGINATION_OBJECT_KEY"] = None
    # app.config['PAGINATE_DATA_OBJECT_KEY'] = "data"

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    pagination.init_app(app, db)

    api.add_namespace(program_level_ns)
    api.add_namespace(course_blocks_ns)
    api.add_namespace(course_statuses_ns)
    api.add_namespace(course_groupes_ns)
    api.add_namespace(specialty_ns)
    api.add_namespace(teachers_ns)
    api.add_namespace(teachers_ns)
    api.add_namespace(school_ns)
    api.add_namespace(university_ns)
    return app
