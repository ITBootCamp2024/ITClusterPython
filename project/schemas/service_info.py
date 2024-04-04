from flask_restx import fields

from project.extensions import api
from project.schemas.departments import short_department_model
from project.schemas.discipline_blocks import short_discipline_blocks_model
from project.schemas.discipline_groups import short_discipline_groups_model
from project.schemas.disciplines import short_discipline_model
from project.schemas.education_levels import education_level_model
from project.schemas.education_programs import short_education_program_model
from project.schemas.position import position_model
from project.schemas.specialty import base_specialty_model
from project.schemas.teachers import teacher_short_model
from project.schemas.universities import short_university_model


university_service_model = api.model(
    "UniversityService",
    {
        **short_university_model,
        "abbr": fields.String(
            required=True,
            description="University abbreviation",
            min_length=1,
            max_length=45,
            default="ABBR"
        ),
        "department": fields.List(fields.Nested(short_department_model))
    }
)


discipline_blocks_service_model = api.model(
    "DisciplineBlocksService",
    {
        **short_discipline_blocks_model,
        "disciplineGroups": fields.List(fields.Nested(short_discipline_groups_model))
    }
)


service_info_model = api.model(
    "ServiceInfo",
    {
        "position": fields.List(fields.Nested(position_model)),
        "education_levels": fields.List(fields.Nested(education_level_model)),
        "teachers": fields.List(fields.Nested(teacher_short_model)),
        "university": fields.List(fields.Nested(university_service_model)),
        "specialty": fields.List(fields.Nested(base_specialty_model)),
        "discipline": fields.List(fields.Nested(short_discipline_model)),
        "disciplineBlocks": fields.List(fields.Nested(discipline_blocks_service_model)),
        "education_program": fields.List(fields.Nested(short_education_program_model)),
    },
)
