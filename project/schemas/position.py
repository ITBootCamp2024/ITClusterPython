from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

short_position_model = api.model(
    "ShortPosition",
    {
        "id": fields.Integer(
            readonly=True,
            description="Position unique identifier",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Position name",
            min_length=1,
            max_length=100,
            default="Position name"
        )
    }
)


position_model = api.model(
    "Position",
    {
        **short_position_model,
        "description": fields.String(
            description="Position description",
        ),
    }
)


paginated_position_model = get_pagination_schema_for(position_model)
