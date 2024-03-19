from flask import Flask

from project.extensions import api, db, migrate
from project.routes.course_blocks import course_blocks
from project.routes.programs_levels import program_level
from project.routes.cities import city
from project.models import ProgramLevel, CourseBlocks


def create_app():
    app = Flask(__name__)

    # Flask to use UTF-8 encoding
    app.config["JSON_AS_ASCII"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(program_level)
    api.add_namespace(course_blocks)
    api.add_namespace(city)
    return app
