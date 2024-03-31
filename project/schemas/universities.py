from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

short_university_model = api.model(
    "ShortUniversity",
    {
        "id": fields.Integer(
            readonly=True,
            description="The unique identifier of the university",
        ),
        "name": fields.String(
            required=True,
            description="Name of the university",
            min_length=3,
            max_length=150,),
    }
)


university_model = api.model(
    "University",
    {
        **short_university_model,
        "abbr": fields.String(
            required=True,
            description="University abbreviation",
            min_length=1,
            max_length=45,
        ),
        "programs_list_url": fields.String(
            required=True,
            description="Url for the list of programs",
            max_length=255
        ),
        "url": fields.String(
            required=True,
            description="University site",
            max_length=255
        )
    }
)


paginated_university_model = get_pagination_schema_for(university_model)
