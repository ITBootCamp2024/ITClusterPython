from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, SyllabusBaseInfo
from project.schemas.authorization import authorizations
from project.schemas.syllabus import (
    syllabus_base_info_model,
    syllabus_base_info_patch_model, not_required_fields_base_info,
)
from project.validators import allowed_roles

syllabuses_ns = Namespace(
    name="syllabuses", description="Syllabuses info", authorizations=authorizations
)


def get_syllabus_or_404(syllabus_id):
    syllabus = Syllabus.query.get(syllabus_id)
    if not syllabus:
        abort(404, f"Syllabus with id {syllabus_id} not found")
    return syllabus


def get_syllabus_base_info_or_404(syllabus_id):
    syllabus_base_info = (
        db.session.query(SyllabusBaseInfo)
        .filter(SyllabusBaseInfo.syllabus_id == syllabus_id)
        .first()
    )

    if not syllabus_base_info:
        abort(404, f"Syllabus with id {syllabus_id} not found")

    return syllabus_base_info


def verify_teacher(syllabus):
    if (get_jwt().get("role") == "teacher" and
            syllabus.teacher.email != get_jwt_identity()):
        abort(403, "You are not the teacher of this syllabus")


@syllabuses_ns.route("/base-info/<int:syllabus_id>")
class BaseSyllabusInfo(Resource):
    @syllabuses_ns.marshal_with(syllabus_base_info_model)
    def get(self, syllabus_id):
        """Get the base info about the syllabus"""
        return get_syllabus_base_info_or_404(syllabus_id)

    @syllabuses_ns.expect(syllabus_base_info_patch_model, validate=False)
    @syllabuses_ns.marshal_with(syllabus_base_info_model)
    @syllabuses_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def patch(self, syllabus_id):
        """Update the base info about the syllabus"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        syllabus_base_info = get_syllabus_base_info_or_404(syllabus_id)

        plain_params = not_required_fields_base_info.keys()
        for key, value in syllabuses_ns.payload.items():
            if key in plain_params:
                setattr(syllabus_base_info, key, value)

        db.session.add(syllabus_base_info)
        db.session.commit()

        return syllabus_base_info
