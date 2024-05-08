from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import DisciplineGroup, DisciplineBlock, Roles
from project.schemas.authorization import authorizations
from project.schemas.discipline_groups import (
    discipline_groups_model,
    discipline_groups_query_model,
)
from project.schemas.service_info import serviced_discipline_groups_model
from project.validators import validate_site, allowed_roles

discipline_groups_ns = Namespace(
    name="discipline-groups",
    description="Discipline groups",
    authorizations=authorizations,
)


def get_discipline_group_or_404(id):
    discipline_group = DisciplineGroup.query.get(id)
    if not discipline_group:
        abort(404, "The discipline group not found")
    return discipline_group


def get_discipline_group_response():
    discipline_groups = DisciplineGroup.query.all()
    discipline_blocks = DisciplineBlock.query.all()
    return {
        "content": discipline_groups,
        "service_info": {
            "disciplineBlocks": discipline_blocks,
        },
        "totalElements": len(discipline_groups),
    }


@discipline_groups_ns.route("")
class DisciplineGroupsList(Resource):
    """Shows a list of all discipline groups, and lets you POST to add new discipline group"""

    @discipline_groups_ns.marshal_with(serviced_discipline_groups_model)
    def get(self):
        """List all discipline groups"""
        return get_discipline_group_response()

    @discipline_groups_ns.expect(discipline_groups_query_model)
    @discipline_groups_ns.marshal_with(serviced_discipline_groups_model)
    @validate_site("http", ["discipline_url"])
    @discipline_groups_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Create a new discipline group"""
        discipline_group = DisciplineGroup()
        plain_params = ["name", "description", "discipline_url"]
        nested_ids = ["block"]
        for key, value in discipline_groups_ns.payload.items():
            if key in plain_params:
                setattr(discipline_group, key, value)
            elif key in nested_ids:
                setattr(discipline_group, key + "_id", value.get("id"))

        db.session.add(discipline_group)
        db.session.commit()
        return get_discipline_group_response()


@discipline_groups_ns.route("/<int:id>")
@discipline_groups_ns.response(404, "The discipline group not found")
@discipline_groups_ns.param("id", "The discipline group unique identifier")
class DisciplineGroupsDetail(Resource):
    """Show a single discipline group and lets you delete them"""

    @discipline_groups_ns.marshal_with(discipline_groups_model)
    def get(self, id):
        """Fetch a discipline group with given id"""
        return get_discipline_group_or_404(id)

    @discipline_groups_ns.expect(discipline_groups_query_model, validate=False)
    @discipline_groups_ns.marshal_with(serviced_discipline_groups_model)
    @validate_site("http", ["discipline_url"])
    @discipline_groups_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id):
        """Update a discipline group with given id"""
        discipline_group = get_discipline_group_or_404(id)
        plain_params = ["name", "description", "discipline_url"]
        nested_ids = ["block"]
        for key, value in discipline_groups_ns.payload.items():
            if key in plain_params:
                setattr(discipline_group, key, value)
            elif key in nested_ids:
                setattr(discipline_group, key + "_id", value.get("id"))
        db.session.commit()
        return get_discipline_group_response()

    @discipline_groups_ns.marshal_with(serviced_discipline_groups_model)
    @discipline_groups_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete a discipline group with given id"""
        discipline_block = get_discipline_group_or_404(id)
        db.session.delete(discipline_block)
        db.session.commit()
        return get_discipline_group_response()
