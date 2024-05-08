from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import (
    Discipline,
    Teacher,
    EducationProgram,
    DisciplineBlock,
    Syllabus,
    SyllabusBaseInfo,
    SyllabusStatus,
    Roles,
)
from project.schemas.authorization import authorizations
from project.schemas.disciplines import discipline_model, discipline_query_model
from project.schemas.service_info import serviced_discipline_model
from project.validators import validate_site, allowed_roles

disciplines_ns = Namespace(
    name="disciplines",
    description="Disciplines information",
    authorizations=authorizations,
)


def get_discipline_or_404(id):
    discipline = Discipline.query.get(id)
    if not discipline:
        abort(404, "Discipline not found")
    return discipline


def get_discipline_response():
    disciplines = Discipline.query.all()
    teachers = Teacher.query.all()
    education_programs = EducationProgram.query.all()
    discipline_blocks = DisciplineBlock.query.all()
    return {
        "content": disciplines,
        "service_info": {
            "teachers": teachers,
            "education_program": education_programs,
            "disciplineBlocks": discipline_blocks,
        },
        "totalElements": len(disciplines),
    }


@disciplines_ns.route("")
class DisciplinesList(Resource):
    """Shows a list of all disciplines, and lets you POST to add new education discipline"""

    @disciplines_ns.marshal_with(serviced_discipline_model)
    def get(self):
        """List all education disciplines"""
        return get_discipline_response()

    # @disciplines_ns.doc(security="jsonWebToken")
    @disciplines_ns.expect(discipline_query_model)
    @disciplines_ns.marshal_with(serviced_discipline_model)
    @validate_site("http", ["syllabus_url", "education_plan_url"])
    @disciplines_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Adds a new education discipline"""
        discipline = Discipline()
        plain_params = ["name", "syllabus_url", "education_plan_url"]
        nested_ids = ["teacher", "discipline_group", "education_program"]
        for key, value in disciplines_ns.payload.items():
            if key in plain_params:
                setattr(discipline, key, value)
            elif key in nested_ids:
                setattr(discipline, key + "_id", value.get("id"))
        db.session.add(discipline)
        db.session.commit()

        syllabus = Syllabus(
            name=discipline.name,
            status=SyllabusStatus.NOT_FILLED,
            discipline_id=discipline.id,
        )
        db.session.add(syllabus)
        db.session.commit()

        syllabus_base_info = SyllabusBaseInfo(
            syllabus_id=syllabus.id,
            specialty_id=discipline.education_program.specialty_id,
        )
        db.session.add(syllabus_base_info)
        db.session.commit()

        return get_discipline_response()


@disciplines_ns.route("/<int:id>")
@disciplines_ns.response(404, "Discipline not found")
@disciplines_ns.param("id", "The discipline's unique identifier")
class DisciplinesDetail(Resource):
    """Show a discipline and lets you delete him"""

    @disciplines_ns.marshal_with(discipline_model)
    def get(self, id):
        """Fetch the discipline with a given id"""
        return get_discipline_or_404(id)

    @disciplines_ns.expect(discipline_query_model, validate=False)
    @disciplines_ns.marshal_with(serviced_discipline_model)
    @validate_site("http", ["syllabus_url", "education_plan_url"])
    @disciplines_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id):
        """Update the discipline with a given id"""
        discipline = get_discipline_or_404(id)
        plain_params = ["name", "syllabus_url", "education_plan_url"]
        nested_ids = ["teacher", "discipline_group", "education_program"]
        for key, value in disciplines_ns.payload.items():
            if key in plain_params:
                setattr(discipline, key, value)
            elif key in nested_ids:
                setattr(discipline, key + "_id", value.get("id"))
        db.session.commit()

        syllabus = discipline.syllabus
        syllabus.name = discipline.name

        base_info = syllabus.base_information_syllabus
        base_info.specialty_id = discipline.education_program.specialty_id

        db.session.commit()

        return get_discipline_response()

    @disciplines_ns.marshal_with(serviced_discipline_model)
    @disciplines_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete the discipline with given id"""
        discipline = get_discipline_or_404(id)
        db.session.delete(discipline)
        db.session.commit()
        # TODO: add logic to delete syllabus and syllabus_base_info
        return get_discipline_response()


# TODO: delete or hide this endpoint after using it
@disciplines_ns.route("/add-syllabuses-to-all-disciplines")
class DisciplinesAddSyllabuses(Resource):

    @disciplines_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        disciplines_without_syllabuses = (
            db.session.query(Discipline)
            .filter(~Discipline.id.in_(db.session.query(Syllabus.discipline_id)))  # noqa
            .all()
        )

        result = []
        for discipline in disciplines_without_syllabuses:
            disdict = dict()
            disdict["discipline"] = {
                "id": discipline.id,
                "name": discipline.name,
            }
            syllabus = Syllabus(
                name=discipline.name, status="Не заповнено", discipline_id=discipline.id
            )
            db.session.add(syllabus)
            db.session.commit()

            disdict["syllabus"] = {
                "id": syllabus.id,
                "name": syllabus.name,
                "status": syllabus.status,
            }

            syllabus_base_info = SyllabusBaseInfo(
                syllabus_id=syllabus.id,
                specialty_id=discipline.education_program.specialty_id,
            )
            db.session.add(syllabus_base_info)
            db.session.commit()

            disdict["syllabus_base_info"] = {
                "id": syllabus_base_info.id,
                "syllabus_id": syllabus_base_info.syllabus_id,
                "specialty_id": syllabus_base_info.specialty_id,
            }

            result.append(disdict)

        return {"disciplines": result, "totalElements": len(result)}
