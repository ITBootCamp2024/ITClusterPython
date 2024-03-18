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

# program_level_input_model = api.model("ProgramLevelInput", {"name": fields.String})


new_schema = api.model()