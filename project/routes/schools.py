from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, api
from project.schema import school_model
from project.models import School

school_ns = Namespace(
    name="schools", description="schools involved in programs"
)


def get_school_or_404(id: int) -> School:
    school = School.query.get(id)
    if not school:
        abort(404, "ID incorrect, school not found")
    return school


@school_ns.route("/")
class SchoolList(Resource):
    """Read a list of all schools, available in our site """
    @school_ns.marshal_list_with(school_model)
    def get(self):
        """List of all schools"""
        return School.query.all()

    @school_ns.expect(school_model)
    @school_ns.marshal_list_with(school_model)
    def post(self) -> tuple:
        """Create a new school"""
        school = School(name=school_ns.payload["name"],
                        size=school_ns.payload["size"],
                        description=school_ns.payload["description"],
                        contact=school_ns.payload["contact"],
                        university_id =school_ns.payload["university_id"],
                        )
        try:
            db.session.add(school)
            db.session.commit()
        except IntegrityError:
            abort(400, "Name/shortname should be unique")
        schools = School.query.all()
        return schools, 201


@school_ns.route("/<int:id>/")
@school_ns.response(404, "Program level not found")
@school_ns.param("id", "The program level unique identifier")
class SchoolDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single school"""

    @school_ns.marshal_with(school_model)
    def get(self, id: int) -> tuple:
        """Fetch a certain school"""
        return get_school_or_404(id), 201

    @school_ns.expect(school_model)
    @school_ns.marshal_list_with(school_model)
    def put(self, id: int) -> tuple:
        """Update a certain school"""
        school = get_school_or_404(id)
        try:
            school.name = school_ns.payload["name"]
            school.name = school_ns.payload["size"]
            school.name = school_ns.payload["description"]
            school.name = school_ns.payload["contact"]
            school.name = school_ns.payload["university_id"]
            db.session.commit()
        except IntegrityError:
            abort(400, "Name should be unique")
        schools = School.query.all()
        return schools, 200

    @school_ns.expect(school_model)
    @school_ns.expect(school_model)
    def delete(self, id: int) -> tuple:
        """Delete a school according to ID"""
        school = get_school_or_404(id)
        db.session.delete(school)
        db.session.commit()
        schools = School.query.all()
        return schools, 200
