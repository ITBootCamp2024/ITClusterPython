from flask_restx import fields

from project.extensions import api
from project.schemas.degree import degree_model
from project.schemas.departments import short_department_model
from project.schemas.general import base_id_model
from project.schemas.pagination import get_pagination_schema_for
from project.schemas.position import position_model
from project.schemas.universities import short_university_model

base_teacher_model = api.model(
    "BaseTeacher",
    {
        "id": fields.Integer(
            readonly=True, description="The teacher unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the teacher",
            min_length=1,
            max_length=100,
        ),
        "email": fields.String(
            required=True,
            description="The teacher's email",
            min_length=0,
            max_length=100,
        ),
        "comments": fields.String(
            required=True,
            description="Some comments to the teacher",
            min_length=0
        )
    }
)

teacher_model = api.model(
    "Teacher",
    {
        **base_teacher_model,
        "position": fields.Nested(position_model),
        "degree": fields.Nested(degree_model),
        "university": fields.Nested(short_university_model),
        "department": fields.Nested(short_department_model),
    }
)


teacher_query_model = api.inherit(
    "TeacherQuery",
    {
        **base_teacher_model,
        "position": fields.Nested(base_id_model, required=True),
        "degree": fields.Nested(base_id_model, required=True),
        "department": fields.Nested(base_id_model, required=True)
    }
)


paginated_teacher_model = get_pagination_schema_for(teacher_model)
