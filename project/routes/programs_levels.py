from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.schema import program_level_model
from project.models import ProgramLevel

program_level = Namespace(
    name="programs_levels", description="Level of the educational program"
)


@program_level.route("/")
class ProgramLevelList(Resource):
    """Shows a list of all programs levels, and lets you POST to add new program level"""

    @program_level.marshal_list_with(program_level_model)
    def get(self):
        """List all programs levels"""
        return ProgramLevel.query.all()

    @program_level.expect(program_level_model)
    @program_level.marshal_list_with(program_level_model)
    def post(self):
        """Create a new programs levels"""
        program = ProgramLevel(name=program_level.payload["name"])
        db.session.add(program)
        db.session.commit()
        return program, 201


def get_program_level_or_404(id):
    program = ProgramLevel.query.get(id)
    if not program:
        abort(404, "Program level not found")
    return program


@program_level.route("/<int:id>/")
@program_level.response(404, "Program level not found")
@program_level.param("id", "The program level unique identifier")
class ProgramLevelDetail(Resource):
    """Show a single program level and lets you delete them"""

    @program_level.marshal_with(program_level_model)
    def get(self, id):
        """Fetch a given program level"""
        return get_program_level_or_404(id)

    @program_level.expect(program_level_model)
    @program_level.marshal_list_with(program_level_model)
    def put(self, id):
        """Update a program level given its identifier"""
        program = get_program_level_or_404(id)
        program.name = program_level.payload["name"]
        db.session.commit()
        return program

    def delete(self, id):
        """Delete a program level given its identifier"""
        program = get_program_level_or_404(id)
        db.session.delete(program)
        db.session.commit()
        return {}, 204
