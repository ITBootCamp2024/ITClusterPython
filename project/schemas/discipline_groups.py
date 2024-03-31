from flask_restx import fields

from project.extensions import api
from project.schemas.general import base_id_model
from project.schemas.discipline_blocks import short_discipline_blocks_model
from project.schemas.pagination import get_pagination_schema_for

base_discipline_groups_model = api.model(
    "BaseDisciplineGroups",
    {
        "id": fields.Integer(
            readonly=True, description="The unique identifier of discipline group"
        ),
        "name": fields.String(
            required=True,
            description="The discipline group name",
            min_length=1,
            max_length=100,
        ),
        "description": fields.String(description="The discipline group description"),
        "discipline_url": fields.String(
            description="The link to the discipline group",
            max_length=255
        )
    }
)


discipline_groups_model = api.model(
    "DisciplineGroup",
    {
        **base_discipline_groups_model,
        "block": fields.Nested(short_discipline_blocks_model)
    },
)


discipline_groups_query_model = api.model(
    "DisciplineGroupsQuery",
    {
        **base_discipline_groups_model,
        "block": fields.Nested(base_id_model, required=True)
    }
)


paginated_discipline_groups_model = get_pagination_schema_for(discipline_groups_model)


