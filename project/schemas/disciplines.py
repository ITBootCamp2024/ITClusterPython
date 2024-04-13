from flask_restx import fields

from project.extensions import api
from project.schemas.discipline_blocks import short_discipline_blocks_model
from project.schemas.discipline_groups import short_discipline_groups_model
from project.schemas.education_programs import short_education_program_model
from project.schemas.general import base_id_model
from project.schemas.pagination import get_pagination_schema_for
from project.schemas.teachers import teacher_short_model

short_discipline_model = api.model(
    "ShortDiscipline",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the discipline",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Discipline name",
            min_length=2,
            max_length=100,
            default="discipline name"
        )
    }
)


base_discipline_model = api.model(
    "BaseDiscipline",
    {
        **short_discipline_model,
        "syllabus_url": fields.String(
            required=True,
            description="Syllabus url",
            max_length=255,
        ),
        "education_plan_url": fields.String(
            required=True,
            description="Education plan url",
            max_length=255,
        )
    }
)


discipline_model = api.model(
    "Discipline",
    {
        **base_discipline_model,
        "teacher": fields.Nested(teacher_short_model, required=True),
        "discipline_block": fields.Nested(short_discipline_blocks_model, required=True),
        "discipline_group": fields.Nested(short_discipline_groups_model, required=True),
        "education_program": fields.Nested(short_education_program_model, required=True)
    }
)


discipline_query_model = api.model(
    "DisciplineQuery",
    {
        **base_discipline_model,
        "teacher": fields.Nested(base_id_model, required=True),
        "discipline_group": fields.Nested(base_id_model, required=True),
        "education_program": fields.Nested(base_id_model, required=True)
    }
)


paginated_discipline_model = get_pagination_schema_for(discipline_model)
