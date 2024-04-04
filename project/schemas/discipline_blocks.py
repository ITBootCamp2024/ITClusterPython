from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

short_discipline_blocks_model = api.model(
    "ShortDisciplineBlocks",
    {
        "id": fields.Integer(readonly=True, description="The unique identifier of discipline block"),
        "name": fields.String(
            required=True,
            description="The discipline block name",
            min_length=1,
            max_length=255,
            default="discipline block name"
        ),
    }
)


discipline_blocks_model = api.model(
    "DisciplineBlock",
    {
        **short_discipline_blocks_model,
        "description": fields.String(
            description="The discipline block description",
        ),
    },
)

paginated_discipline_blocks_model = get_pagination_schema_for(discipline_blocks_model)
