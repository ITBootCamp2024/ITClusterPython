from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

degree_model = api.model(
    "Degree",
    {
        "id": fields.Integer(
            readonly=True, description="Degree unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="Degree name",
            min_length=1,
            max_length=45,
        )
    }
)


paginated_degree_model = get_pagination_schema_for(degree_model)
