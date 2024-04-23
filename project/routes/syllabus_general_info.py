from flask_restx import Resource, Namespace

from project.routes.assessment import get_assessment_response
from project.routes.discipline_info import get_discipline_info_response
from project.routes.discipline_structure import get_syllabus_structure_three_response
from project.routes.market_relation import get_market_relation_response
from project.routes.syllabus import get_syllabus_base_info_response, syllabuses_ns
from project.schemas.syllabus_general_info import syllabus_general_info_response_model

gen_info_ns = Namespace("general-info", description="General info about the syllabus")


def get_syllabus_general_info_response(syllabus_id):
    return {
        **get_syllabus_base_info_response(syllabus_id),
        **get_market_relation_response(syllabus_id),
        **get_discipline_info_response(syllabus_id),
        "discipline_structure": {**get_syllabus_structure_three_response(syllabus_id)},
        **get_assessment_response(syllabus_id),
    }


@syllabuses_ns.route("/general-info/<int:syllabus_id>")
@syllabuses_ns.param("syllabus_id", "The syllabus unique identifier")
class GeneralSyllabusInfo(Resource):

    @syllabuses_ns.marshal_with(
        syllabus_general_info_response_model, envelope="content"
    )
    def get(self, syllabus_id):
        """Get the general info about the syllabus by given syllabus id"""
        return get_syllabus_general_info_response(syllabus_id)
