from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import University, Roles
from project.schemas.authorization import authorizations
from project.schemas.service_info import serviced_university_model
from project.schemas.universities import university_model
from project.validators import validate_site, allowed_roles

university_ns = Namespace(
    name="universities",
    description="university with appropriate programs",
    authorizations=authorizations,
)


def get_university_or_404(id):
    university = University.query.get(id)
    if not university:
        abort(404, "Incorrect ID, not found")
    return university


def get_university_response():
    universities = University.query.all()
    return {"content": universities, "totalElements": len(universities)}


@university_ns.route("")
class UniversitylList(Resource):
    """Shows a list of all universities, available in our site"""

    @university_ns.marshal_with(serviced_university_model)
    def get(self):
        """List of all universities"""

        return get_university_response()

    @university_ns.expect(university_model)
    @university_ns.marshal_with(serviced_university_model)
    @validate_site("http", ["url", "programs_list_url"])
    @university_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Create a new university"""
        university = University(
            name=university_ns.payload["name"],
            url=university_ns.payload["url"],
            abbr=university_ns.payload["abbr"],
            programs_list_url=university_ns.payload["programs_list_url"],
        )
        db.session.add(university)
        db.session.commit()
        return get_university_response()


@university_ns.route("/<int:id>")
@university_ns.response(404, "Incorrect ID, not found")
@university_ns.param("id", "University  ID")
class UniversityDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single university"""

    @university_ns.marshal_with(university_model)
    def get(self, id: int) -> University:
        """Fetch a given University"""
        return get_university_or_404(id)

    @university_ns.expect(university_model, validate=False)
    @university_ns.marshal_with(serviced_university_model)
    @validate_site("http", ["url", "programs_list_url"])
    @university_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id: int):
        """Update a certain university"""
        university = get_university_or_404(id)
        uni_keys = university_model.keys()

        for key, value in university_ns.payload.items():
            if key in uni_keys:
                setattr(university, key, value)

        db.session.commit()
        return get_university_response()

    @university_ns.marshal_with(serviced_university_model)
    @university_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id: int):
        """Delete the University according to ID"""
        university = get_university_or_404(id)
        db.session.delete(university)
        db.session.commit()
        return get_university_response()
