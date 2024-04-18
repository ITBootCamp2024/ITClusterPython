from flask_restx import fields, reqparse

from project.extensions import api
from project.schemas.disciplines import short_discipline_model
from project.schemas.syllabus import base_syllabus_model
from project.schemas.teachers import teacher_short_model


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
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the teacher",
            default=1
        ),
        **base_course_model
    }
)

course_with_name_model = api.model(
    "CourseWithName",
    {
        **teacher_short_model,
        **base_course_model
    }
)


teacher_id_parser = reqparse.RequestParser()
teacher_id_parser.add_argument("teacher_id", type=int, required=False)
