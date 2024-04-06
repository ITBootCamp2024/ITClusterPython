from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

short_university_model = api.model(
    "ShortUniversity",
    {
        "id": fields.Integer(
            readonly=True,
            description="The unique identifier of the university",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Name of the university",
            min_length=3,
            max_length=150,
            default="university name"
        )
    }
)


base_university_model = api.model(
    "BaseUniversity",
    {
        **short_university_model,
        "abbr": fields.String(
            required=True,
            description="University abbreviation",
            min_length=1,
            max_length=45,
            default="ABBR"
        ),
    }
)

university_model = api.model(
    "University",
    {
        **base_university_model,
        "programs_list_url": fields.String(
            required=True,
            description="Url for the list of programs",
            max_length=255,
            default="http://programs-list-url"
        ),
        "url": fields.String(
            required=True,
            description="University site",
            max_length=255,
            default="http://example.com"
        )
    }
)


paginated_university_model = get_pagination_schema_for(university_model)
