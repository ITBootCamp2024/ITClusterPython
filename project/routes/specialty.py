from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Specialty
from project.schemas.service_info import serviced_specialty_model
from project.schemas.specialty import specialty_model
from project.validators import validate_site


specialty_ns = Namespace(name="specialties", description="Specialties")


def get_specialty_or_404(id):
    specialty = Specialty.query.get(id)
    if not specialty:
        abort(404, "Specialty not found")
    return specialty


def get_specialty_response():
    specialties = Specialty.query.all()
    return {
        "content": specialties,
        "totalElements": len(specialties)
    }


@specialty_ns.route("")
class SpecialtyList(Resource):
    """Shows a list of all specialties, and lets you POST to add new specialties"""

    @specialty_ns.marshal_with(serviced_specialty_model)
    def get(self):
        """List all specialties"""
        return get_specialty_response()

    @specialty_ns.expect(specialty_model)
    @specialty_ns.marshal_with(serviced_specialty_model)
    @validate_site('http', ["standard_url"])
    def post(self):
        """Create a new specialty"""
        specialty = Specialty()
        for key, value in specialty_ns.payload.items():
            setattr(specialty, key, value)
        db.session.add(specialty)
        db.session.commit()
        return get_specialty_response()


@specialty_ns.route("/<int:id>")
@specialty_ns.response(404, "Specialty not found")
@specialty_ns.param("id", "The specialty unique identifier")
class SpecialtyDetail(Resource):
    """Show a single specialty and lets you delete it"""

    @specialty_ns.marshal_with(specialty_model)
    def get(self, id):
        """Fetch specialty with the given identifier"""
        return get_specialty_or_404(id)

    @specialty_ns.expect(specialty_model, validate=False)
    @specialty_ns.marshal_with(serviced_specialty_model)
    @validate_site('http', ["standard_url"])
    def patch(self, id):
        """Update a specialty with the given identifier"""
        specialty = get_specialty_or_404(id)
        specialty_keys = specialty_model.keys()
        for key, value in specialty_ns.payload.items():
            if key in specialty_keys:
                setattr(specialty, key, value)
        db.session.commit()
        return get_specialty_response()

    @specialty_ns.marshal_with(serviced_specialty_model)
    def delete(self, id):
        """Delete a specialty given its identifier"""
        specialty = get_specialty_or_404(id)
        db.session.delete(specialty)
        db.session.commit()
        return get_specialty_response()
