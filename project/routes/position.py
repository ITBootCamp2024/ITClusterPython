from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Position, Roles
from project.schemas.authorization import authorizations
from project.schemas.position import position_model
from project.schemas.service_info import serviced_position_model
from project.validators import allowed_roles

position_ns = Namespace(
    name="position", description="positions of teachers", authorizations=authorizations
)


def get_position_or_404(id):
    position = Position.query.get(id)
    if not position:
        abort(404, "Position not found")
    return position


def get_position_response():
    positions = Position.query.all()
    return {"content": positions, "totalElements": len(positions)}


@position_ns.route("")
class PositionList(Resource):
    """Shows a list of all positions, and lets you POST to add new position"""

    @position_ns.marshal_with(serviced_position_model)
    def get(self):
        """List all positions"""
        return get_position_response()

    @position_ns.expect(position_model)
    @position_ns.marshal_with(serviced_position_model)
    @position_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Adds a new position"""
        position = Position()
        for key, value in position_ns.payload.items():
            setattr(position, key, value)
        db.session.add(position)
        db.session.commit()
        return get_position_response()


@position_ns.route("/<int:id>")
@position_ns.response(404, "Position not found")
@position_ns.param("id", "The position's unique identifier")
class PositionsDetail(Resource):
    """Show a position and lets you delete and modify it"""

    @position_ns.marshal_with(position_model)
    def get(self, id):
        """Fetch the position with a given id"""
        return get_position_or_404(id)

    @position_ns.expect(position_model, validate=False)
    @position_ns.marshal_with(serviced_position_model)
    @position_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id):
        """Update the position with a given id"""
        position = get_position_or_404(id)
        position_keys = position_model.keys()
        for key, value in position_ns.payload.items():
            if key in position_keys:
                setattr(position, key, value)
        db.session.commit()
        return get_position_response()

    @position_ns.marshal_with(serviced_position_model)
    @position_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete the position with a given id"""
        position = get_position_or_404(id)
        db.session.delete(position)
        db.session.commit()
        return get_position_response()
