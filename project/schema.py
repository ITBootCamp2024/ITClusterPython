from project.extensions import api
from flask_restx import fields

program_level_model = api.model(
    "ProgramLevel",
    {
        "id": fields.Integer(
            readonly=True, description="The program level unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The program level name",
            min_length=1,
            max_length=100,
        ),
    },
)

course_blocks_model = api.model(
    "CourseBlocks",
    {
        "id": fields.Integer(readonly=True, description="The course unique identifier"),
        "name": fields.String(
            required=True, description="The course name", min_length=1, max_length=100
        ),
        "description": fields.String(
            required=True, description="The course description"
        ),
    },
)

course_statuses_model = api.model(
    "CourseStatuses",
    {
        "id": fields.Integer(readonly=True, description="The status unique identifier"),
        "name": fields.String(
            required=True, description="The status name", min_length=1, max_length=100
        ),
        "description": fields.String(description="The status description"),
    },
)

course_groupes_model = api.model(
    "CourseGroupes",
    {
        "id": fields.Integer(
            readonly=True, description="The course_group unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The course_group name",
            min_length=1,
            max_length=100,
        ),
        "description": fields.String(description="The course_group description"),
        "type_id": fields.Integer(min=1),
    },
)

specialty_model = api.model(
    "Specialty",
    {
        "id": fields.Integer(
            required=True, description="The specialty unique identifier", min=0, max=500
        ),
        "name": fields.String(
            required=True,
            description="The name of the specialty",
            min_length=1,
            max_length=200,
        ),
        "link_standart": fields.String(
            required=True,
            description="The link to the specialty",
            min_length=0,
            max_length=200,
        ),
    },
)

teacher_model = api.model(
    "Teacher",
    {
        "id": fields.Integer(
            readonly=True, description="The teacher unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the teacher",
            min_length=1,
            max_length=50,
        ),
        "role": fields.String(
            required=True,
            description="The role of the teacher",
            min_length=1,
            max_length=50,
        ),
        "status": fields.String(
            required=True,
            description="The status of the teacher",
            min_length=0,
            max_length=100,
        ),
        "email": fields.String(
            required=True,
            description="The email of the teacher",
            min_length=0,
            max_length=100,
        ),
        "details": fields.String(
            required=True,
            description="The details of the teacher",
            min_length=0,
            max_length=100,
        ),
    },
)

pagination_parser = api.parser()
pagination_parser.add_argument(
    "page", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "size", type=int, required=False, default=20, help="Page size (number of items per page)"
)
