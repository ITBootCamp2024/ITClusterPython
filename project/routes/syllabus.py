from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, Discipline, SyllabusBaseInfo
from project.schemas.authorization import authorizations
from project.schemas.service_info import service_info_for_base_syllabus_model
from project.schemas.syllabus import (
    syllabus_base_info_query_model,
    syllabus_base_info_model,
    syllabus_base_info_patch_model,
)
from project.validators import allowed_roles

syllabuses_ns = Namespace(
    name="syllabuses", description="Syllabuses info", authorizations=authorizations
)


def get_syllabus_base_info_or_404(syllabus_id):
    syllabus_base_info = (
        db.session.query(SyllabusBaseInfo)
        .filter(SyllabusBaseInfo.syllabus_id == syllabus_id)
        .first()
    )

    if not syllabus_base_info:
        abort(404, f"Syllabus with id {syllabus_id} not found")

    return syllabus_base_info


@syllabuses_ns.route("/create")
class SyllabusesCreate(Resource):
    """Create a new syllabus"""

    @syllabuses_ns.expect(syllabus_base_info_query_model)
    @syllabuses_ns.marshal_with(syllabus_base_info_model)
    @syllabuses_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def post(self):
        """Create a new syllabus and base info about it"""

        discipline_id = syllabuses_ns.payload.get("discipline").get("id")
        discipline = Discipline.query.filter_by(id=discipline_id).first()

        if not discipline:
            abort(400, f"Discipline with id {discipline_id} not found")

        if discipline.syllabus:
            abort(400, f"Discipline with id {discipline_id} already has a syllabus")

        user_role = get_jwt().get("role")
        if user_role == "teacher" and discipline.teacher.email != get_jwt_identity():
            abort(403, "You are not the teacher of this discipline")

        syllabus = Syllabus(
            name=discipline.name, status="Не заповнено", discipline_id=discipline_id
        )
        db.session.add(syllabus)
        db.session.commit()

        specialty_id = syllabuses_ns.payload.get("specialty").get("id")
        syllabus_base_info = SyllabusBaseInfo(
            syllabus_id=syllabus.id,
            specialty_id=specialty_id,
        )
        db.session.add(syllabus_base_info)
        db.session.commit()
        return syllabus_base_info


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

        user_role = get_jwt().get("role")
        if user_role == "teacher":
            teacher_email = Syllabus.query.get(syllabus_id).teacher.email
            if teacher_email != get_jwt_identity():
                abort(403, "You are not the teacher of this syllabus")

        syllabus_base_info = get_syllabus_base_info_or_404(syllabus_id)

        plain_params = ["student_count", "course", "semester"]
        for key, value in syllabuses_ns.payload.items():
            if key in plain_params:
                setattr(syllabus_base_info, key, value)

        db.session.add(syllabus_base_info)
        db.session.commit()

        return syllabus_base_info


@syllabuses_ns.route("/base-syllabus-service-info/<int:teacher_id>")
class BaseSyllabusServiceInfo(Resource):
    """Get the base info to create or modify the syllabus"""

    @syllabuses_ns.response(200, "Success", service_info_for_base_syllabus_model)
    def get(self, teacher_id):
        """Get the info for creating or modifying the syllabus"""
        disciplines_without_syllabuses = (
            db.session.query(Discipline)
            .filter(Discipline.teacher_id == teacher_id)
            .filter(~Discipline.id.in_(db.session.query(Syllabus.discipline_id)))
            .all()
        )

        sps = {}

        for discipline in disciplines_without_syllabuses:
            # specialty_id
            spid = discipline.education_program.specialty_id
            # education_program_id
            epid = discipline.education_program_id
            # block_id
            blid = discipline.discipline_block.id

            specialty_code = discipline.education_program.specialty.code
            specialty_name = discipline.education_program.specialty.name
            program_name = discipline.education_program.name
            block_name = discipline.discipline_block.name

            if spid not in sps:
                sps[spid] = {
                    "id": spid,
                    "code": specialty_code,
                    "name": specialty_name,
                    "eps": {},  # educational programs
                }

            if epid not in sps[spid]["eps"]:
                sps[spid]["eps"][epid] = {
                    "id": epid,
                    "name": program_name,
                    "dbs": {},  # discipline blocks
                }

            if blid not in sps[spid]["eps"][epid]["dbs"]:
                sps[spid]["eps"][epid]["dbs"][blid] = {
                    "id": blid,
                    "name": block_name,
                    "ds": [],  # disciplines
                }

            sps[spid]["eps"][epid]["dbs"][blid]["ds"].append(
                {"id": discipline.id, "name": discipline.name}
            )

        specialties_list = [
            {
                "id": specialty_id,
                "code": data["code"],
                "name": data["name"],
                "educational_programs": [
                    {
                        "id": pr_id,
                        "name": pr_data["name"],
                        "discipline_blocks": [
                            {
                                "id": bl_id,
                                "name": bl_data["name"],
                                "disciplines": bl_data["ds"],
                            }
                            for bl_id, bl_data in pr_data["dbs"].items()
                        ],
                    }
                    for pr_id, pr_data in data["eps"].items()
                ],
            }
            for specialty_id, data in sps.items()
        ]

        return {"specialties": specialties_list}
