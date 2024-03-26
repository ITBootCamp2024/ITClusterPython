from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.schema import (
    school_model,
    pagination_parser,
    custom_schema_pagination,
    get_pagination_schema_for,
)
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
    @school_ns.expect(pagination_parser)
    @school_ns.marshal_with(get_pagination_schema_for(school_model))
    def get(self):
        """List of all schools"""
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )

    @school_ns.expect(pagination_parser)
    @school_ns.marshal_with(get_pagination_schema_for(school_model))
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
            abort(400, "Name should be unique")
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )


@school_ns.route("/<int:id>/")
@school_ns.response(404, "School not found")
@school_ns.param("id", "School ID")
class SchoolDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single school"""

    @school_ns.marshal_with(school_model)
    def get(self, id: int) -> tuple:
        """Fetch a certain school"""
        return get_school_or_404(id), 201

    @school_ns.expect(school_model)
    @school_ns.marshal_with(get_pagination_schema_for(school_model))
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
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )

    @school_ns.expect(school_model)
    @school_ns.marshal_with(get_pagination_schema_for(school_model))
    def delete(self, id: int) -> tuple:
        """Delete a school according to ID"""
        school = get_school_or_404(id)
        db.session.delete(school)
        db.session.commit()
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )
