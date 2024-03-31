from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

position_model = api.model(
    "Position",
    {
        "id": fields.Integer(
            readonly=True, description="Position unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="Position name",
            min_length=1,
            max_length=100,
        )
    }
)


paginated_position_model = get_pagination_schema_for(position_model)
