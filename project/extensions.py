from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_rest_paginate import Pagination
from flask_jwt_extended import JWTManager

api = Api(
    title="API ITClusterPython",
    version="1.0",
    description="All API metadatas",
)
db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()
pagination = Pagination()
jwt = JWTManager()
mail = Mail()
