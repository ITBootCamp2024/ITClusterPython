from flask_restx import fields

from project.extensions import api
from project.schemas.degree import degree_model
from project.schemas.departments import short_department_model
from project.schemas.discipline_blocks import short_discipline_blocks_model
from project.schemas.discipline_groups import short_discipline_groups_model
from project.schemas.disciplines import short_discipline_model
from project.schemas.education_levels import education_level_model
from project.schemas.position import position_model
from project.schemas.specialty import base_specialty_model
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


service_info_model = api.model(
    "ServiceInfo",
    {
        "position": fields.List(fields.Nested(position_model)),
        "degree": fields.List(fields.Nested(degree_model)),
        "university": fields.List(fields.Nested(university_service_model)),
        "specialty": fields.List(fields.Nested(base_specialty_model)),
        "educationLevels": fields.List(fields.Nested(education_level_model)),
        "discipline": fields.List(fields.Nested(short_discipline_model)),
        "disciplineGroups": fields.List(fields.Nested(short_discipline_groups_model)),
        "disciplineBlocks": fields.List(fields.Nested(short_discipline_blocks_model))
    }
)
