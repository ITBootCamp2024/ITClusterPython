from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.models import DisciplineBlock
from project.schemas.discipline_blocks import paginated_discipline_blocks_model, discipline_blocks_model
from project.schemas.pagination import pagination_parser, custom_schema_pagination

discipline_blocks_ns = Namespace(
    name="discipline-blocks", description="Discipline blocks info"
)


@discipline_blocks_ns.route("")
# @discipline_blocks_ns.response(200, model=[discipline_blocks_model], description="Success")
class DisciplineBlocksList(Resource):
    """Shows a list of all discipline blocks, and lets you POST to add new discipline block"""

    @discipline_blocks_ns.expect(pagination_parser)
    @discipline_blocks_ns.marshal_with(paginated_discipline_blocks_model)
    def get(self):
        """List all discipline blocks"""
        return pagination.paginate(
            DisciplineBlock,
            discipline_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @discipline_blocks_ns.expect(discipline_blocks_model, pagination_parser)
    @discipline_blocks_ns.marshal_with(paginated_discipline_blocks_model)
    def post(self):
        """Create a new discipline block"""
        discipline_block = DisciplineBlock()
        for key, value in discipline_blocks_ns.payload.items():
            setattr(discipline_block, key, value)
        db.session.add(discipline_block)
        db.session.commit()
        return pagination.paginate(
            DisciplineBlock,
            discipline_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )


def get_discipline_block_or_404(id):
    discipline_block = DisciplineBlock.query.get(id)
    if not discipline_block:
        abort(404, "Discipline block not found")
    return discipline_block


@discipline_blocks_ns.route("/<int:id>")
# @discipline_blocks_ns.response(200, model=[discipline_blocks_model], description="Success")
@discipline_blocks_ns.response(404, "Discipline block not found")
@discipline_blocks_ns.param("id", "The discipline block unique identifier")
class DisciplineBlocksDetail(Resource):
    """Show a single discipline block and lets you delete them"""

    @discipline_blocks_ns.marshal_with(discipline_blocks_model)
    def get(self, id):
        """Fetch a discipline block with given id"""
        return get_discipline_block_or_404(id)

    @discipline_blocks_ns.expect(discipline_blocks_model, pagination_parser, validate=False)
    @discipline_blocks_ns.marshal_with(paginated_discipline_blocks_model)
    def patch(self, id):
        """Update a discipline block with given id"""
        discipline_block = get_discipline_block_or_404(id)
        discipline_block_keys = discipline_blocks_model.keys()
        for key, value in discipline_blocks_ns.payload.items():
            if key in discipline_block_keys:
                setattr(discipline_block, key, value)
        db.session.commit()
        return pagination.paginate(
            DisciplineBlock,
            discipline_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @discipline_blocks_ns.expect(pagination_parser)
    @discipline_blocks_ns.marshal_with(paginated_discipline_blocks_model)
    def delete(self, id):
        """Delete a discipline block with given id"""
        discipline_block = get_discipline_block_or_404(id)
        db.session.delete(discipline_block)
        db.session.commit()
        return pagination.paginate(
            DisciplineBlock,
            discipline_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )
