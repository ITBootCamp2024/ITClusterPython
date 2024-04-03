from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

education_level_model = api.model(
    "EducationLevel",
    {
        "id": fields.Integer(
            readonly=True, description="Unique identifier of the education level"
        ),
        "education_level": fields.String(
            required=True,
            description="Education level",
            max_length=45,
            default="education level",
        ),
        "name": fields.String(
            required=True,
            description="Education level name",
            max_length=45,
            default="education level name",
        )
    }
)


paginated_education_level_model = get_pagination_schema_for(education_level_model)
