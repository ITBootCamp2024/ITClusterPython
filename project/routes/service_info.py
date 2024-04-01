from flask_restx import Resource, Namespace

from project.models import (
    Degree,
    Discipline,
    DisciplineBlock,
    DisciplineGroup,
    EducationLevel,
    Position,
    Specialty,
    University,
)
from project.schemas.service_info import service_info_model

service_info_ns = Namespace(name="service_info", description="Service information")


@service_info_ns.route("")
class ServiceInfo(Resource):
    @service_info_ns.marshal_with(service_info_model)
    def get(self):
        positions = Position.query.all()
        degrees = Degree.query.all()
        universities = University.query.all()
        specialties = Specialty.query.all()
        education_levels = EducationLevel.query.all()
        disciplines = Discipline.query.all()
        discipline_groups = DisciplineGroup.query.all()
        discipline_blocks = DisciplineBlock.query.all()

        return {
            "position": positions,
            "degree": degrees,
            "university": universities,
            "specialty": specialties,
            "educationLevels": education_levels,
            "discipline": disciplines,
            "disciplineGroups": discipline_groups,
            "disciplineBlocks": discipline_blocks
        }, 200
