from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, Discipline, SyllabusBaseInfo
from project.schemas.authorization import authorizations
from project.schemas.syllabus import syllabus_base_info_query_model, syllabus_base_info_model
from project.validators import allowed_roles


syllabuses_ns = Namespace(name="syllabuses",
                          description="Syllabuses info",
                          authorizations=authorizations)


@syllabuses_ns.route("/create")
class SyllabusesCreate(Resource):
    """ Create a new syllabus """
    @allowed_roles(["teacher", "admin", "content_manager"])
    @syllabuses_ns.doc(security="jsonWebToken")
    @syllabuses_ns.expect(syllabus_base_info_query_model)
    @syllabuses_ns.marshal_with(syllabus_base_info_model)
    def post(self):
        """ Create a new syllabus and base info about it"""
        # TODO: Implement creation of syllabus
        discipline_id = syllabuses_ns.payload.get("discipline").get("id")
        discipline = Discipline.query.filter_by(id=discipline_id).first()

        if not discipline:
            abort(400, f"Discipline with id {discipline_id} not found")

        if discipline.syllabus:
            abort(400, f"Discipline with id {discipline_id} already has a syllabus")

        user_role = get_jwt().get("role")
        if user_role == "teacher" and discipline.teacher.email != get_jwt_identity():
            abort(403, "You are not the teacher of this discipline")

        syllabus = Syllabus(name=discipline.name,
                            status="Не заповнено",
                            discipline_id=discipline_id)
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


@syllabuses_ns.route("/base-syllabus-service-info")
class BaseSyllabusServiceInfo(Resource):
    """ Get the base info to create or modify the syllabus """

    def get(self):
        """ Get the info for creating or modifying the syllabus """
        # TODO: Implement base info for creating or modifying the syllabus
        pass

