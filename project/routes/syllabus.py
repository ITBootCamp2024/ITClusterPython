from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, SyllabusBaseInfo
from project.schemas.authorization import authorizations
from project.schemas.syllabus import (
    syllabus_base_info_response_model,
    syllabus_base_info_patch_model,
    not_required_fields_base_info,
)
from project.validators import allowed_roles, verify_teacher

syllabuses_ns = Namespace(
    name="syllabuses", description="Syllabuses info", authorizations=authorizations
)


def get_syllabus_or_404(syllabus_id):
    syllabus = Syllabus.query.get(syllabus_id)
    if not syllabus:
        abort(404, f"Syllabus with id {syllabus_id} not found")
    return syllabus


def get_syllabus_base_info_response(syllabus_id):
    syllabus_base_info = (
        db.session.query(SyllabusBaseInfo)
        .filter(SyllabusBaseInfo.syllabus_id == syllabus_id)
        .first()
    )

    if not syllabus_base_info:
        abort(404, f"Syllabus with id {syllabus_id} not found")

    return {
        "base_info": syllabus_base_info,
        "syllabus_id": syllabus_id,
    }


@syllabuses_ns.route("/base-info/<int:syllabus_id>")
@syllabuses_ns.param("syllabus_id", "The syllabus unique identifier")
class BaseSyllabusInfo(Resource):
    @syllabuses_ns.marshal_with(syllabus_base_info_response_model, envelope="content")
    def get(self, syllabus_id):
        """Get the base info about the syllabus"""
        return get_syllabus_base_info_response(syllabus_id)

    @syllabuses_ns.expect(syllabus_base_info_patch_model, validate=False)
    @syllabuses_ns.marshal_with(syllabus_base_info_response_model, envelope="content")
    @syllabuses_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def patch(self, syllabus_id):
        """Update the base info about the syllabus"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        syllabus_base_info = syllabus.base_information_syllabus

        plain_params = not_required_fields_base_info.keys()
        for key, value in syllabuses_ns.payload.items():
            if key in plain_params:
                setattr(syllabus_base_info, key, value)

        db.session.add(syllabus_base_info)
        db.session.commit()

        return get_syllabus_base_info_response(syllabus_id)
