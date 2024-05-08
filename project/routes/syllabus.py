from flask import jsonify
from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import (
    Syllabus,
    SyllabusBaseInfo,
    Roles,
    MarketRelation,
    DisciplineInfo,
    SyllabusModule,
    SelfStudyTopic,
    GraduateTask,
    SyllabusStatus,
    Assessment,
)
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


def set_syllabus_filling_status(syllabus_id):
    """Set the syllabus status ot FILLED if all tables are filled. Else set it to ON_FILLING"""

    syllabus = get_syllabus_or_404(syllabus_id)

    tables = [MarketRelation, DisciplineInfo, SyllabusModule, SelfStudyTopic, GraduateTask, Assessment]

    not_filled_table_exists = False
    filled_table_exists = False

    for table in tables:
        if table.query.filter_by(syllabus_id=syllabus_id).first():
            filled_table_exists = True
        else:
            not_filled_table_exists = True
        if filled_table_exists and not_filled_table_exists:
            syllabus.status = SyllabusStatus.ON_FILLING
            db.session.commit()
            return

    if filled_table_exists:
        syllabus.status = SyllabusStatus.FILLED
    else:
        syllabus.status = SyllabusStatus.NOT_FILLED

    db.session.commit()


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
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
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


@syllabuses_ns.route("/set-all-filling-statuses")
class SetAllFillingStatuses(Resource):

    @syllabuses_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN])
    def post(self):
        """Set all filling statuses"""
        response = []

        syllabuses = Syllabus.query.all()
        for syllabus in syllabuses:
            status_before = syllabus.status
            set_syllabus_filling_status(syllabus.id)
            response.append(
                {
                    "syllabus_id": syllabus.id,
                    "status_before": status_before,
                    "status_after": syllabus.status,
                    "name": syllabus.name,
                }
            )

        return jsonify({"syllabuses": response})
