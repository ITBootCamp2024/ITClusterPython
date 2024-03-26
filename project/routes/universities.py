from flask import request
from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.schema import (
    university_model,
    pagination_parser,
    custom_schema_pagination,
    get_pagination_schema_for,
)
from project.models import University


university_ns = Namespace(
    name="universities", description="university with appropriate programs"
)


def get_uni_or_404(id):
    uni = University.query.get(id)
    if not uni:
        abort(404, "Incorrect ID, not found")
    return uni


def validate_site(value: str, parametres: list):
    """Decorator to validate if a parameter starts with a specified value."""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            for n in parametres:
                param_value = request.json.get(n)
                if not param_value or not param_value.startswith(value):
                    abort(400, f"Invalid {n}. It must start with '{value}'.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@university_ns.route("")
class UniversitylList(Resource):
    """Shows a list of all universities, available in our site """

    @university_ns.expect(pagination_parser)
    @university_ns.marshal_with(get_pagination_schema_for(university_model))
    def get(self):
        """List of all universities"""

        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )

    @university_ns.expect(university_model)
    @university_ns.marshal_with(get_pagination_schema_for(university_model))
    @validate_site('http', ["sitelink", "programs_list"])
    def post(self):
        """Create a new university"""
        university = University(name=university_ns.payload["name"],
                                sitelink=university_ns.payload["sitelink"],
                                shortname=university_ns.payload["shortname"],
                                programs_list=university_ns.payload["programs_list"],
                                )
        try:
            db.session.add(university)
            db.session.commit()
        except IntegrityError:
            abort(400, "Name/shortname should be unique")
        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )


@university_ns.route("/<int:id>")
@university_ns.response(404, "University not found")
@university_ns.param("id", "University  ID")
class UniversityDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single university"""

    @university_ns.marshal_with(university_model)
    def get(self, id: int) -> University:
        """Fetch a given University"""
        return get_uni_or_404(id)

    @university_ns.expect(university_model)
    @university_ns.marshal_with(get_pagination_schema_for(university_model))
    def patch(self, id: int) -> tuple:
        """Update a certain university"""
        university = get_uni_or_404(id)

        fields_to_update = ["name", "sitelink", "shortname", "programs_list"]

        try:
            for field in fields_to_update:
                if field in university_ns.payload:
                    setattr(university, field, university_ns.payload[field])

            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "Name/shortname should be unique")
        finally:
            db.session.close()

        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )

    @university_ns.expect(pagination_parser)
    @university_ns.marshal_with(get_pagination_schema_for(university_model))
    def delete(self, id: int):
        """Delete the University according to ID"""
        university = get_uni_or_404(id)
        db.session.delete(university)
        db.session.commit()
        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )
