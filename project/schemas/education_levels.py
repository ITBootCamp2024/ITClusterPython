from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for


short_education_level_model = api.model(
    "ShortEducationLevel",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the education level",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Education level name",
            max_length=45,
            default="education level name",
        )
    }
)


education_level_model = api.model(
    "EducationLevel",
    {
        **short_education_level_model,
        "education_level": fields.String(
            required=True,
            description="Education level",
            max_length=45,
            default="education level",
        )
    }
)


paginated_education_level_model = get_pagination_schema_for(education_level_model)
