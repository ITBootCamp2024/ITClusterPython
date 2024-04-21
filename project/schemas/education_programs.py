from flask_restx import fields

from project.extensions import api
from project.schemas.departments import short_department_model_with_url
from project.schemas.education_levels import education_level_model
from project.schemas.general import base_id_model
from project.schemas.pagination import get_pagination_schema_for
from project.schemas.specialty import short_specialty_model
from project.schemas.universities import short_university_model


primary_education_program_model = api.model(
    "PrimaryEducationProgram",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the education program",
            default=1,
        ),
        "name": fields.String(
            required=True,
            description="Education program name",
            min_length=2,
            max_length=100,
            default="education program name",
        ),
    },
)


short_education_program_model = api.model(
    "ShortEducationProgram",
    {
        **primary_education_program_model,
        "program_url": fields.String(
            required=True,
            description="Education program url",
            max_length=255,
            default="http://education-program.url",
        ),
    },
)


base_education_program_model = api.model(
    "BaseEducationProgram",
    {
        **short_education_program_model,
        "guarantor": fields.String(
            required=True,
            description="Guarantor name",
            max_length=100,
            default="guarantor name",
        ),
        "syllabus_url": fields.String(
            required=True,
            description="Syllabus url",
            max_length=255,
            default="http://syllabus-url",
        ),
    },
)


education_program_model = api.model(
    "EducationProgram",
    {
        **base_education_program_model,
        "specialty": fields.Nested(short_specialty_model, required=True),
        "university": fields.Nested(short_university_model, required=True),
        "education_level": fields.Nested(education_level_model, required=True),
        "department": fields.Nested(short_department_model_with_url, required=True),
    },
)


education_program_query_model = api.model(
    "EducationProgramQuery",
    {
        **base_education_program_model,
        "specialty": fields.Nested(base_id_model, required=True),
        "education_level": fields.Nested(base_id_model, required=True),
        "department": fields.Nested(base_id_model, required=True),
    },
)


# program_parser = api.parser()
# program_parser.add_argument(
#     "specialty_id", type=int, required=False, default=0, help="Specialty ID"
# )
# program_parser.add_argument(
#     "university_id", type=int, required=False, default=0, help="University ID"
# )
# program_parser.add_argument(
#     "level", type=int, required=False, default=0, help="Level ID"
# )


paginated_education_program_model = get_pagination_schema_for(education_program_model)
