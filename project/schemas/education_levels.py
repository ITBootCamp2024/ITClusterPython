from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

education_level_model = api.model(
    "EducationLevel",
    {
        "id": fields.Integer(
            readonly=True, description="Unique identifier of the education level"
        ),
        "name": fields.String(
            required=True,
            description="Education level name",
            min_length=1,
            max_length=45,
            default="education level",
        )
    }
)


paginated_education_level_model = get_pagination_schema_for(education_level_model)
