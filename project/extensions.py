from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

api = Api(
    title="API ITClusterPython",
    version="1.0",
    description="All API metadatas",
)
db = SQLAlchemy()
migrate = Migrate()
