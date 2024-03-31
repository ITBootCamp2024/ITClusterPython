from flask_restx import fields

from project.extensions import api
from project.schemas.pagination import get_pagination_schema_for

program_model = api.model(
    "Program",
    {
        "id": fields.Integer(
            readonly=True, description="The program's unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the program",
            min_length=1,
            max_length=200,
        ),
        "specialty_id": fields.Integer(
            required=True,
            description="id of the specialty",
            min=1
        ),
        "program_link": fields.String(
            required=True,
            description="The link to the program",
            min_length=0,
            max_length=200,
        ),
        "university_id": fields.Integer(
            required=True,
            description="id of the university",
            min=1
        ),
        "level": fields.Integer(
            required=True,
            description="id of the level",
            min=1
        ),
        "garant": fields.String(
            required=True,
            description="Garant's name",
            min_length=0,
            max_length=100,
        ),
        "school_name": fields.String(
            required=True,
            description="The name of the school",
            min_length=0,
            max_length=200,
        ),
        "school_link": fields.String(
            required=True,
            description="The school's link",
            min_length=0,
            max_length=200,
        ),
        "clabus_link": fields.String(
            required=True,
            description="The clabus's link",
            min_length=0,
            max_length=200,
        )
    }
)


program_parser = api.parser()
program_parser.add_argument(
    "specialty_id", type=int, required=False, default=0, help="Specialty ID"
)
program_parser.add_argument(
    "university_id", type=int, required=False, default=0, help="University ID"
)
program_parser.add_argument(
    "level", type=int, required=False, default=0, help="Level ID"
)


paginated_program_model = get_pagination_schema_for(program_model)

