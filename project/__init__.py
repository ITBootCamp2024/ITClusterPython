from flask import Flask

from project.extensions import api, db, migrate
from project.routes.programs_levels import program_level
from project.routes.cities import city
from project.routes.specialty import specialty_ns
from project.models import ProgramLevel


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://sql8692454:Qz3t2dTcb9@sql8.freesqldatabase.com:3306/sql8692454"

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api.add_namespace(program_level)
    api.add_namespace(city)
    api.add_namespace(specialty_ns)
    return app
