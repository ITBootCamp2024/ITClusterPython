from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import DisciplineBlock, Roles
from project.schemas.authorization import authorizations
from project.schemas.discipline_blocks import discipline_blocks_model
from project.schemas.service_info import serviced_discipline_blocks_model
from project.validators import allowed_roles

discipline_blocks_ns = Namespace(
    name="discipline-blocks",
    description="Discipline blocks info",
    authorizations=authorizations,
)


def get_discipline_block_or_404(id):
    discipline_block = DisciplineBlock.query.get(id)
    if not discipline_block:
        abort(404, "Discipline block not found")
    return discipline_block


def get_discipline_block_response():
    discipline_blocks = DisciplineBlock.query.all()
    return {"content": discipline_blocks, "totalElements": len(discipline_blocks)}


@discipline_blocks_ns.route("")
class DisciplineBlocksList(Resource):
    """Shows a list of all discipline blocks, and lets you POST to add new discipline block"""

    @discipline_blocks_ns.marshal_with(serviced_discipline_blocks_model)
    def get(self):
        """List all discipline blocks"""
        return get_discipline_block_response()

    @discipline_blocks_ns.expect(discipline_blocks_model)
    @discipline_blocks_ns.marshal_with(serviced_discipline_blocks_model)
    @discipline_blocks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Create a new discipline block"""
        discipline_block = DisciplineBlock()
        for key, value in discipline_blocks_ns.payload.items():
            setattr(discipline_block, key, value)
        db.session.add(discipline_block)
        db.session.commit()
        return get_discipline_block_response()


@discipline_blocks_ns.route("/<int:id>")
@discipline_blocks_ns.response(404, "Discipline block not found")
@discipline_blocks_ns.param("id", "The discipline block unique identifier")
class DisciplineBlocksDetail(Resource):
    """Show a single discipline block and lets you delete them"""

    @discipline_blocks_ns.marshal_with(discipline_blocks_model)
    def get(self, id):
        """Fetch a discipline block with given id"""
        return get_discipline_block_or_404(id)

    @discipline_blocks_ns.expect(discipline_blocks_model, validate=False)
    @discipline_blocks_ns.marshal_with(serviced_discipline_blocks_model)
    @discipline_blocks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id):
        """Update a discipline block with given id"""
        discipline_block = get_discipline_block_or_404(id)
        discipline_block_keys = discipline_blocks_model.keys()
        for key, value in discipline_blocks_ns.payload.items():
            if key in discipline_block_keys:
                setattr(discipline_block, key, value)
        db.session.commit()
        return get_discipline_block_response()

    @discipline_blocks_ns.marshal_with(serviced_discipline_blocks_model)
    @discipline_blocks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete a discipline block with given id"""
        discipline_block = get_discipline_block_or_404(id)
        db.session.delete(discipline_block)
        db.session.commit()
        return get_discipline_block_response()
