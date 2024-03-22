from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.schema import (
    program_level_model,
    pagination_parser,
    custom_schema_pagination,
)
from project.models import ProgramLevel

program_level_ns = Namespace(
    name="programs_levels", description="Level of the educational program"
)


@program_level_ns.route("/")
@program_level_ns.response(200, model=[program_level_model], description="Success")
class ProgramLevelList(Resource):
    """Shows a list of all programs levels, and lets you POST to add new program level"""

    @program_level_ns.expect(pagination_parser)
    def get(self):
        """List all programs levels"""
        return pagination.paginate(
            ProgramLevel,
            program_level_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @program_level_ns.expect(program_level_model, pagination_parser)
    def post(self):
        """Create a new programs levels"""
        program = ProgramLevel(name=program_level_ns.payload["name"])
        db.session.add(program)
        db.session.commit()
        return pagination.paginate(
            ProgramLevel,
            program_level_model,
            pagination_schema_hook=custom_schema_pagination,
        )


def get_program_level_or_404(id):
    program = ProgramLevel.query.get(id)
    if not program:
        abort(404, "Program level not found")
    return program


@program_level_ns.route("/<int:id>/")
@program_level_ns.response(200, model=[program_level_model], description="Success")
@program_level_ns.response(404, "Program level not found")
@program_level_ns.param("id", "The program level unique identifier")
class ProgramLevelDetail(Resource):
    """Show a single program level and lets you delete them"""

    @program_level_ns.marshal_with(program_level_model)
    def get(self, id):
        """Fetch a given program level"""
        return get_program_level_or_404(id)

    @program_level_ns.expect(program_level_model, pagination_parser)
    def put(self, id):
        """Update a program level given its identifier"""
        program = get_program_level_or_404(id)
        program.name = program_level_ns.payload["name"]
        db.session.commit()
        return pagination.paginate(
            ProgramLevel,
            program_level_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @program_level_ns.expect(pagination_parser)
    def delete(self, id):
        """Delete a program level given its identifier"""
        program = get_program_level_or_404(id)
        db.session.delete(program)
        db.session.commit()
        return pagination.paginate(
            ProgramLevel,
            program_level_model,
            pagination_schema_hook=custom_schema_pagination,
        )
