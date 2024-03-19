from project.extensions import api
from flask_restx import fields

program_level_model = api.model(
    "ProgramLevel",
    {
        "id": fields.Integer(
            readonly=True, description="The program level unique identifier"
        ),
        "name": fields.String(required=True, description="The program level name"),
    },
)

course_blocks_model = api.model(
    "CourseBlocks",
    {
        "id": fields.Integer(readonly=True, description="The course unique identifier"),
        "name": fields.String(required=True, description="The course name"),
        "description": fields.String(
            required=True, description="The course description"
        ),
    },
)

# program_level_input_model = api.model("ProgramLevelInput", {"name": fields.String})


specialty_model = api.model(
    "Specialty",
    {
        "id": fields.Integer(readonly=True, description="The specialty unique identifier"),
        "name": fields.String(required=True, description="The name of the specialty"),
        "link_standart": fields.String(
            required=True, description="The link to the specialty"
        ),
    },
)