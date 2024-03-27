from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.routes.universities import validate_site
from project.schema import (
    school_model,
    pagination_parser,
    custom_schema_pagination,
    get_pagination_schema_for, paginated_school_model,
)
from project.models import School, University

school_ns = Namespace(
    name="schools", description="university's schools"
)


def get_school_or_404(id: int) -> School:
    school = School.query.get(id)
    if not school:
        abort(404, "ID incorrect, school not found")
    return school


def validate_uni_id(f):
    def decorated_function(*args, **kwargs):
        payload = school_ns.payload
        university_id = payload.get('university_id')
        # Check if university_id exists in the database
        if not university_id:
            return f(*args, **kwargs)
        if not University.query.filter_by(id=university_id).first():
            abort(400, "Invalid university ID")
        return f(*args, **kwargs)
    return decorated_function


@school_ns.route("")
class SchoolList(Resource):
    """Read a list of all schools, available in our site """
    @school_ns.expect(pagination_parser)
    @school_ns.marshal_with(get_pagination_schema_for(school_model))
    def get(self):
        """List of all schools"""
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )

    @school_ns.expect(school_model)
    @school_ns.marshal_with(paginated_school_model)
    @validate_uni_id
    @validate_site('http', ["site"])
    def post(self) -> tuple:
        """Create a new school"""
        school = School(name=school_ns.payload["name"],
                        site=school_ns.payload["site"],
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


@school_ns.route("/<int:id>")
@school_ns.response(404, "School not found")
@school_ns.param("id", "School ID")
class SchoolDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single school"""

    @school_ns.marshal_with(school_model)
    def get(self, id: int) -> tuple:
        """Fetch a certain school"""
        return get_school_or_404(id), 201

    @school_ns.expect(school_model, pagination_parser, validates=False)
    @school_ns.marshal_with(paginated_school_model)
    @validate_site('http', ["site"])
    @validate_uni_id
    def patch(self, id: int) -> tuple:
        """Update a certain school"""
        school = get_school_or_404(id)
        school_keys = school_model.keys()

        try:
            for key, value in school_ns.payload.items():
                if key in school_keys:
                    setattr(school, key, value)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "Name should be unique")
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )

    @school_ns.expect(pagination_parser)
    @school_ns.marshal_with(paginated_school_model)
    def delete(self, id: int) -> tuple:
        """Delete a school according to ID"""
        school = get_school_or_404(id)
        db.session.delete(school)
        db.session.commit()
        return pagination.paginate(
            School, school_model, pagination_schema_hook=custom_schema_pagination
        )
