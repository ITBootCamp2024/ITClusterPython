from flask_restx import fields

from project.extensions import api
from project.schemas.courses import course_model
from project.schemas.departments import short_department_model, department_model
from project.schemas.discipline_blocks import (
    short_discipline_blocks_model,
    discipline_blocks_model,
)
from project.schemas.discipline_groups import (
    short_discipline_groups_model,
    discipline_groups_model,
)
from project.schemas.disciplines import short_discipline_model, discipline_model
from project.schemas.education_levels import education_level_model
from project.schemas.education_programs import (
    short_education_program_model,
    education_program_model,
)
from project.schemas.position import position_model, short_position_model
from project.schemas.specialty import base_specialty_model, specialty_model
from project.schemas.teachers import teacher_short_model, teacher_model
from project.schemas.universities import (
    short_university_model,
    university_model,
    base_university_model,
)

university_service_model = api.model(
    "UniversityService",
    {
        **short_university_model,
        "abbr": fields.String(
            required=True,
            description="University abbreviation",
            min_length=1,
            max_length=45,
            default="ABBR",
        ),
        "department": fields.List(fields.Nested(short_department_model)),
    },
)

discipline_blocks_service_model = api.model(
    "DisciplineBlocksService",
    {
        **short_discipline_blocks_model,
        "disciplineGroups": fields.List(fields.Nested(short_discipline_groups_model)),
    },
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

service_info_for_department = api.model(
    "ServiceInfoForDepartment",
    {"university": fields.List(fields.Nested(base_university_model))},
)

service_info_for_discipline = api.model(
    "ServiceInfoForDiscipline",
    {
        "teachers": fields.List(fields.Nested(teacher_short_model)),
        "education_program": fields.List(fields.Nested(short_education_program_model)),
        "disciplineBlocks": fields.List(fields.Nested(discipline_blocks_service_model)),
    },
)

service_info_for_discipline_group = api.model(
    "ServiceInfoForDisciplineGroup",
    {"disciplineBlocks": fields.List(fields.Nested(short_discipline_blocks_model))},
)

service_info_for_education_program = api.model(
    "ServiceInfoForEducationProgram",
    {
        "specialty": fields.List(fields.Nested(base_specialty_model)),
        "university": fields.List(fields.Nested(university_service_model)),
        "education_levels": fields.List(fields.Nested(education_level_model)),
    },
)

service_info_for_teacher = api.model(
    "ServiceInfoForTeacher",
    {
        "position": fields.List(fields.Nested(short_position_model)),
        "university": fields.List(fields.Nested(university_service_model)),
    },
)

serviced_course_model = api.model(
    "ServicedCourse",
    {
        "content": fields.List(fields.Nested(course_model)),
        "totalElements": fields.Integer(description="The total number of courses"),
    },
)

serviced_department_model = api.model(
    "ServicedDepartment",
    {
        "content": fields.List(fields.Nested(department_model)),
        "service_info": fields.Nested(service_info_for_department),
        "totalElements": fields.Integer(description="The total number of departments"),
    },
)

serviced_discipline_blocks_model = api.model(
    "ServicedDisciplineBlocks",
    {
        "content": fields.List(fields.Nested(discipline_blocks_model)),
        "totalElements": fields.Integer(
            description="The total number of discipline blocks"
        ),
    },
)

serviced_discipline_groups_model = api.model(
    "ServicedDisciplineGroups",
    {
        "content": fields.List(fields.Nested(discipline_groups_model)),
        "service_info": fields.Nested(service_info_for_discipline_group),
        "totalElements": fields.Integer(
            description="The total number of discipline groups"
        ),
    },
)

serviced_discipline_model = api.model(
    "ServicedDiscipline",
    {
        "content": fields.List(fields.Nested(discipline_model)),
        "service_info": fields.Nested(service_info_for_discipline),
        "totalElements": fields.Integer(description="The total number of disciplines"),
    },
)

serviced_education_level_model = api.model(
    "ServicedEducationLevel",
    {
        "content": fields.List(fields.Nested(education_level_model)),
        "totalElements": fields.Integer(
            description="The total number of education levels"
        ),
    },
)

serviced_education_program_model = api.model(
    "ServicedEducationProgram",
    {
        "content": fields.List(fields.Nested(education_program_model)),
        "service_info": fields.Nested(service_info_for_education_program),
        "totalElements": fields.Integer(
            description="The total number of education programs"
        ),
    },
)

serviced_position_model = api.model(
    "ServicedPosition",
    {
        "content": fields.List(fields.Nested(position_model)),
        "totalElements": fields.Integer(description="The total number of positions"),
    },
)

serviced_specialty_model = api.model(
    "ServicedSpecialty",
    {
        "content": fields.List(fields.Nested(specialty_model)),
        "totalElements": fields.Integer(description="The total number of specialties"),
    },
)

serviced_teacher_model = api.model(
    "ServicedTeacher",
    {
        "content": fields.List(fields.Nested(teacher_model)),
        "service_info": fields.Nested(service_info_for_teacher),
        "totalElements": fields.Integer(description="The total number of teachers"),
    },
)

serviced_university_model = api.model(
    "ServicedUniversity",
    {
        "content": fields.List(fields.Nested(university_model)),
        "totalElements": fields.Integer(description="The total number of universities"),
    },
)
