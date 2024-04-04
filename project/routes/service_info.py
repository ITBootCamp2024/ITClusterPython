from flask_restx import Resource, Namespace

from project.models import (
    Discipline,
    DisciplineBlock,
    EducationLevel,
    Position,
    Specialty,
    University,
    Teacher,
    EducationProgram,
)
from project.schemas.service_info import service_info_model

service_info_ns = Namespace(name="service_info", description="Service information")


@service_info_ns.route("")
class ServiceInfo(Resource):
    @service_info_ns.marshal_with(service_info_model)
    def get(self):
        positions = Position.query.all()
        universities = University.query.all()
        specialties = Specialty.query.all()
        education_levels = EducationLevel.query.all()
        disciplines = Discipline.query.all()
        discipline_blocks = DisciplineBlock.query.all()
        teachers = Teacher.query.all()
        education_program = EducationProgram.query.all()

        return {
            "position": positions,
            "education_levels": education_levels,
            "teachers": teachers,
            "university": universities,
            "specialty": specialties,
            "discipline": disciplines,
            "disciplineBlocks": discipline_blocks,
            "education_program": education_program,
        }, 200
