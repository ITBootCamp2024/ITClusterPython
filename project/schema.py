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

specialty_model = api.model(
    "Specialty",
    {
        "id": fields.Integer(
            required=True, description="The specialty unique identifier"
        ),
        "name": fields.String(required=True, description="The name of the specialty"),
        "link_standart": fields.String(
            required=True, description="The link to the specialty"
        ),
    },
)
