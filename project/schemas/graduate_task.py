from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model

graduate_task_model = api.model(
    "GraduateTask",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the graduate task",
            default=1,
        ),
        "name": fields.String(
            required=True,
            description="Graduate task name",
            max_length=255,
            default="graduate task name",
        ),
        "controls": fields.String(
            description="Methods of graduate task control",
        ),
        "deadlines": fields.String(
            description="Graduate task deadlines",
        ),
    },
)

graduate_task_response_model = api.model(
    "GraduateTaskResponse",
    {
        "graduate_tasks": fields.List(
            fields.Nested(graduate_task_model), required=True
        ),
        **syllabus_id_model,
    },
)
