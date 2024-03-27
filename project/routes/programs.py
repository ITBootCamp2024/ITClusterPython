from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.models import Program
from project.schema import (
    program_model,
    pagination_parser,
    custom_schema_pagination,
    paginated_program_model
)


programs_ns = Namespace(name="programs", description="info about programs")


@programs_ns.route("")
class ProgramsList(Resource):
    """Shows a list of all programs, and lets you POST to add new program"""

    @programs_ns.expect(pagination_parser)
    @programs_ns.marshal_with(paginated_program_model)
    def get(self):
        """List all programs"""
        return pagination.paginate(
            Program, program_model, pagination_schema_hook=custom_schema_pagination
        )

    @programs_ns.expect(program_model, pagination_parser)
    @programs_ns.marshal_with(paginated_program_model)
    def post(self):
        """Add a new program"""
        program = Program()
        for key, value in programs_ns.payload.items():
            setattr(program, key, value)
        db.session.add(program)
        db.session.commit()
        return pagination.paginate(
            Program, program_model, pagination_schema_hook=custom_schema_pagination
        )


def get_program_or_404(id):
    program = Program.query.get(id)
    if not program:
        abort(404, "Program not found")
    return program


@programs_ns.route("/<int:id>")
@programs_ns.response(404, "Program not found")
@programs_ns.param("id", "The program unique identifier")
class ProgramsDetail(Resource):
    """Show a single program and lets you modify and delete it"""

    @programs_ns.marshal_with(program_model)
    def get(self, id):
        """Fetch a given program"""
        return get_program_or_404(id)

    @programs_ns.expect(program_model, pagination_parser, validate=False)
    @programs_ns.marshal_with(paginated_program_model)
    def patch(self, id):
        """Update the program with a given id"""
        program = get_program_or_404(id)
        program_keys = program_model.keys()
        for key, value in programs_ns.payload.items():
            if key in program_keys:
                setattr(program, key, value)
        return pagination.paginate(
            Program, program_model, pagination_schema_hook=custom_schema_pagination
        )

    @programs_ns.expect(pagination_parser)
    @programs_ns.marshal_with(paginated_program_model)
    def delete(self, id):
        """Delete the program with given id"""
        program = get_program_or_404(id)
        db.session.delete(program)
        db.session.commit()
        return pagination.paginate(
            Program, program_model, pagination_schema_hook=custom_schema_pagination
        )
