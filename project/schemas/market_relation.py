from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model

market_relation_model = api.model(
    "MarketRelation",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the market relation",
            default=1,
        ),
        "specialty": fields.String(description="Specialty/profession"),
        "vacancies": fields.String(description="Vacancies"),
        "skills": fields.String(description="Skills"),
        "relevant_materials": fields.String(description="Relevant materials"),
        "borrowed_materials": fields.String(description="Borrowed materials"),
    },
)


market_relation_response_model = api.model(
    "MarketRelationResponse",
    {
        "market_relations": fields.List(
            fields.Nested(market_relation_model), required=True
        ),
        **syllabus_id_model,
    },
)
