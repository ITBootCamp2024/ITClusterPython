from flask_restx import fields

from project.extensions import api
from project.schemas.discipline_blocks import short_discipline_blocks_model
from project.schemas.disciplines import short_discipline_model
from project.schemas.education_programs import short_education_program_model
from project.schemas.general import base_id_model
from project.schemas.specialty import base_specialty_model

short_syllabus_model = api.model(
    "ShortSyllabus",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the syllabus",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Syllabus name",
            max_length=255,
            default="syllabus name"
        )
    }
)

base_syllabus_model = api.model(
    "BaseSyllabus",
    {
        **short_syllabus_model,
        "status": fields.String(
            required=True,
            description="Status of the syllabus",
            max_length=45,
        )
    }
)

syllabus_model = api.model(
    "Syllabus",
    {
        **base_syllabus_model,
        "discipline": fields.Nested(short_discipline_model, required=True)
    }
)

syllabus_base_info_query_model = api.model(
    "SyllabusBaseInfoQuery",
    {
        "discipline": fields.Nested(base_id_model, required=True),
        "specialty": fields.Nested(base_id_model, required=True),
    }
)

syllabus_base_info_model = api.model(
    "SyllabusBaseInfo",
    {
        "syllabus_id": fields.Integer(
            required=True,
            description="Unique identifier of the syllabus",
            default=1
        ),
        "specialty": fields.Nested(base_specialty_model),
        "education_program": fields.Nested(short_education_program_model),
        "discipline_block": fields.Nested(short_discipline_blocks_model),
        "discipline": fields.Nested(short_discipline_model),
        "student_count": fields.Integer(description="Number of students"),
        "course": fields.Integer(description="Year of the study"),
        "semester": fields.Integer(description="Semester of the study")
    }
)
