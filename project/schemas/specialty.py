from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for


short_specialty_model = api.model(
    "ShortSpecialty",
    {
        "id": fields.Integer(
            readonly=True, description="The specialty unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the specialty",
            min_length=1,
            max_length=100,
            default="specialty name"
        )
    }
)


base_specialty_model = api.model(
    "BaseSpecialty",
    {
        **short_specialty_model,
        "code": fields.String(
            required=True,
            description="The code of the specialty",
            max_length=45,
            default="specialty code"
        )
    }
)


specialty_model = api.model(
    "Specialty",
    {
        **base_specialty_model,
        "standard_url": fields.String(
            description="The link to the specialty",
            max_length=255,
            default="http://standard-url"
        ),
    },
)


paginated_specialty_model = get_pagination_schema_for(specialty_model)

