from flask_restx import fields

from project.extensions import api
from project.schemas.departments import short_department_model
from project.schemas.general import base_id_model
from project.schemas.pagination import get_pagination_schema_for
from project.schemas.position import short_position_model
from project.schemas.role import role_model
from project.schemas.universities import short_university_model


teacher_short_model = api.model(
    "TeacherShort",
    {
        "id": fields.Integer(
            readonly=True,
            description="The teacher unique identifier",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="The name of the teacher",
            min_length=1,
            max_length=100,
            default="Teacher Name"
        )
    }
)

base_teacher_model = api.model(
    "BaseTeacher",
    {
        **teacher_short_model,
        "email": fields.String(
            required=True,
            description="The teacher's email",
            min_length=0,
            max_length=100,
            default="teacher@email.com"
        ),
        "degree_level": fields.String(
            description="The teacher's degree level",
            max_length=50
        ),
        "comments": fields.String(
            required=True,
            description="Some comments to the teacher",
        )
    }
)

teacher_model = api.model(
    "Teacher",
    {
        **base_teacher_model,
        "position": fields.Nested(short_position_model, required=True),
        "university": fields.Nested(short_university_model, required=True),
        "department": fields.Nested(short_department_model, required=True),
        "role": fields.Nested(role_model, required=True)
    }
)


teacher_query_model = api.inherit(
    "TeacherQuery",
    {
        **base_teacher_model,
        "position": fields.Nested(base_id_model, required=True),
        "department": fields.Nested(base_id_model, required=True)
    }
)


paginated_teacher_model = get_pagination_schema_for(teacher_model)
