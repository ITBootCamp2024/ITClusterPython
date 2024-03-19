from os import environ

from dotenv import load_dotenv
from flask import Flask

from project.extensions import api, db, migrate
from project.routes.programs_levels import program_level
from project.routes.cities import city
from project.models import ProgramLevel


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(program_level)
    api.add_namespace(city)
    return app
