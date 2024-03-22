from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_rest_paginate import Pagination

api = Api(
    title="API ITClusterPython",
    version="1.0",
    description="All API metadatas",
)
db = SQLAlchemy()
migrate = Migrate()
pagination = Pagination()
