from os import environ

from dotenv import load_dotenv
from flask import Flask

from project.extensions import api, db, migrate
from project.routes.course_blocks import course_blocks
from project.routes.programs_levels import program_level
from project.routes.specialty import specialty_ns
from project.models import ProgramLevel, Specialty, CourseBlocks


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(program_level)
    api.add_namespace(course_blocks)
    api.add_namespace(specialty_ns)
    return app
