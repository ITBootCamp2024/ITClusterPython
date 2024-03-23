from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.models import Specialty
from project.schema import specialty_model, pagination_parser, custom_schema_pagination

specialty_ns = Namespace(name="specialty", description="Specialties")


@specialty_ns.route("/")
class SpecialtyList(Resource):
    """Shows a list of all specialties, and lets you POST to add new specialties"""

    @specialty_ns.expect(pagination_parser)
    def get(self):
        """List all specialties"""
        return pagination.paginate(
            Specialty, specialty_model, pagination_schema_hook=custom_schema_pagination
        )

    @specialty_ns.expect(specialty_model, pagination_parser)
    @specialty_ns.response(400, "Specialty already exists")
    def post(self):
        """Create a new specialty"""
        specialty_id = specialty_ns.payload["id"]
        specialty = Specialty.query.get(specialty_id)
        if specialty:
            abort(400, "Specialty already exists")
        specialty = Specialty(
            id=specialty_id,
            name=specialty_ns.payload["name"],
            link_standart=specialty_ns.payload["link_standart"],
        )
        db.session.add(specialty)
        db.session.commit()
        return pagination.paginate(
            Specialty, specialty_model, pagination_schema_hook=custom_schema_pagination
        )


def get_specialty_or_404(id):
    specialty = Specialty.query.get(id)
    if not specialty:
        abort(404, "Specialty not found")
    return specialty


@specialty_ns.route("/<int:id>/")
@specialty_ns.response(404, "Specialty not found")
@specialty_ns.param("id", "The specialty unique identifier")
class SpecialtyDetail(Resource):
    """Show a single specialty and lets you delete it"""

    @specialty_ns.marshal_with(specialty_model)
    def get(self, id):
        """Fetch specialty with the given identifier"""
        return get_specialty_or_404(id)

    @specialty_ns.expect(specialty_model, pagination_parser)
    def put(self, id):
        """Update a specialty with the given identifier"""
        specialty = get_specialty_or_404(id)
        specialty.name = specialty_ns.payload["name"]
        specialty.link_standart = specialty_ns.payload["link_standart"]
        db.session.commit()
        return pagination.paginate(
            Specialty, specialty_model, pagination_schema_hook=custom_schema_pagination
        )

    @specialty_ns.expect(pagination_parser)
    def delete(self, id):
        """Delete a specialty given its identifier"""
        specialty = get_specialty_or_404(id)
        db.session.delete(specialty)
        db.session.commit()
        return pagination.paginate(
            Specialty, specialty_model, pagination_schema_hook=custom_schema_pagination
        )
