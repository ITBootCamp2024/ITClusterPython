from flask import Flask

from app.extensions import api, db, migrate
from app.routes.programs_levels import program_level
from app.routes.cities import city
from app.models import ProgramLevel


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(program_level)
    api.add_namespace(city)
    return app
