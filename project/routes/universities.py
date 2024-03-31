from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.models import University
from project.schemas.pagination import pagination_parser, custom_schema_pagination
from project.schemas.universities import paginated_university_model, university_model
from project.validators import validate_site

university_ns = Namespace(
    name="universities", description="university with appropriate programs"
)


def get_uni_or_404(id):
    uni = University.query.get(id)
    if not uni:
        abort(404, "Incorrect ID, not found")
    return uni


@university_ns.route("")
class UniversitylList(Resource):
    """Shows a list of all universities, available in our site """

    @university_ns.expect(pagination_parser)
    @university_ns.marshal_with(paginated_university_model)
    def get(self):
        """List of all universities"""

        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )

    @university_ns.expect(university_model)
    @university_ns.marshal_with(paginated_university_model)
    @validate_site('http', ["url", "programs_list_url"])
    def post(self):
        """Create a new university"""
        university = University(name=university_ns.payload["name"],
                                url=university_ns.payload["url"],
                                abbr=university_ns.payload["abbr"],
                                programs_list_url=university_ns.payload["programs_list_url"],
                                )
        try:
            db.session.add(university)
            db.session.commit()
        except IntegrityError:
            db.rollback()
            abort(400, "Name/abbr should be unique")
        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )


@university_ns.route("/<int:id>")
@university_ns.response(404, "Incorrect ID, not found")
@university_ns.param("id", "University  ID")
class UniversityDetail(Resource):
    """Endpoints allow to retrieve detail info, updating and  deleting single university"""

    @university_ns.marshal_with(university_model)
    def get(self, id: int) -> University:
        """Fetch a given University"""
        return get_uni_or_404(id)

    @university_ns.expect(university_model, pagination_parser, validate=False)
    @university_ns.marshal_with(paginated_university_model)
    @validate_site('http', ["url", "programs_list_url"])
    def patch(self, id: int) -> tuple:
        """Update a certain university"""
        university = get_uni_or_404(id)
        uni_keys = university_model.keys()

        try:
            for key, value in university_ns.payload.items():
                if key in uni_keys:
                    setattr(university, key, value)

            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "Name/abbr should be unique")
        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )

    @university_ns.expect(pagination_parser)
    @university_ns.marshal_with(paginated_university_model)
    def delete(self, id: int):
        """Delete the University according to ID"""
        university = get_uni_or_404(id)
        db.session.delete(university)
        db.session.commit()
        return pagination.paginate(
            University, university_model, pagination_schema_hook=custom_schema_pagination
        )
