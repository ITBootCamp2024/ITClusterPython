from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import DisciplineInfo, Roles
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.authorization import authorizations
from project.schemas.discipline_info import (
    discipline_info_response_model,
    discipline_info_model,
)
from project.validators import allowed_roles, verify_teacher

discipline_info_ns = Namespace(
    "syllabuses/discipline-info",
    description="Discipline info",
    authorizations=authorizations,
)


def get_discipline_info_or_404(syllabus_id):
    discipline_info = (
        db.session.query(DisciplineInfo).filter_by(syllabus_id=syllabus_id).first()
    )
    if not discipline_info:
        abort(404, f"Discipline info with syllabus_id {syllabus_id} not found")
    return discipline_info


def get_discipline_info_response(syllabus_id):
    discipline_info = (
        db.session.query(DisciplineInfo).filter_by(syllabus_id=syllabus_id).first()
    )
    return {
        "discipline_info": discipline_info,
        "syllabus_id": syllabus_id,
    }


@discipline_info_ns.route("/<int:syllabus_id>")
@discipline_info_ns.param("syllabus_id", "The syllabus unique identifier")
class DisciplineInfoList(Resource):
    """Get discipline info or create a new discipline info"""

    @discipline_info_ns.marshal_with(discipline_info_response_model, envelope="content")
    def get(self, syllabus_id):
        """Get discipline info by given syllabus_id"""
        return get_discipline_info_response(syllabus_id)

    @discipline_info_ns.expect(discipline_info_model)
    @discipline_info_ns.marshal_with(discipline_info_response_model, envelope="content")
    @discipline_info_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, syllabus_id):
        """Create a new discipline info"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        discipline_info = DisciplineInfo.query.filter_by(syllabus_id=syllabus_id).first()
        if not discipline_info:
            discipline_info = DisciplineInfo(syllabus_id=syllabus_id)
            db.session.add(discipline_info)
            db.session.commit()

        params = discipline_info_model.keys()
        for key, value in discipline_info_ns.payload.items():
            if key in params:
                setattr(discipline_info, key, value)

        db.session.commit()

        set_syllabus_filling_status(syllabus_id)

        return get_discipline_info_response(syllabus_id)

    @discipline_info_ns.expect(discipline_info_model)
    @discipline_info_ns.marshal_with(discipline_info_response_model, envelope="content")
    @discipline_info_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, syllabus_id):
        """Modify discipline info"""

        discipline_info = get_discipline_info_or_404(syllabus_id)
        syllabus = discipline_info.syllabus
        verify_teacher(syllabus)

        params = discipline_info_model.keys()
        for key, value in discipline_info_ns.payload.items():
            if key in params:
                setattr(discipline_info, key, value)
        db.session.commit()

        set_syllabus_filling_status(syllabus_id)

        return get_discipline_info_response(syllabus_id)

    @discipline_info_ns.marshal_with(discipline_info_response_model, envelope="content")
    @discipline_info_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, syllabus_id):
        """Delete discipline info"""

        discipline_info = get_discipline_info_or_404(syllabus_id)
        syllabus = discipline_info.syllabus
        verify_teacher(syllabus)

        db.session.delete(discipline_info)
        db.session.commit()

        set_syllabus_filling_status(syllabus_id)

        return get_discipline_info_response(syllabus_id)
