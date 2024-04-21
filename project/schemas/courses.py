from flask_restx import fields

from project.extensions import api
from project.schemas.disciplines import short_discipline_model
from project.schemas.syllabus import base_syllabus_model

base_course_model = api.model(
    "BaseCourse",
    {
        "discipline": fields.Nested(short_discipline_model),
        "syllabus": fields.Nested(base_syllabus_model)
    }
)

course_model = api.model(
    "Course",
    {
        "teacher_id": fields.Integer(
            readonly=True,
            description="Unique identifier of the teacher",
            default=1
        ),
        **base_course_model
    }
)
