from flask_restx import fields

from project.extensions import api
from project.schemas.assessment import assessment_response_model
from project.schemas.discipline_info import discipline_info_response_model
from project.schemas.discipline_structure import syllabus_structure_three_model
from project.schemas.market_relation import market_relation_response_model
from project.schemas.syllabus import syllabus_base_info_response_model

syllabus_general_info_response_model = api.model(
    "SyllabusGeneralInfoResponse",
    {
        **syllabus_base_info_response_model,
        **market_relation_response_model,
        **discipline_info_response_model,
        "discipline_structure": fields.Nested(syllabus_structure_three_model),
        **assessment_response_model,
    }
)
