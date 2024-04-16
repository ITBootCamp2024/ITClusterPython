from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import jwt_required

from project.extensions import db, pagination
from project.models import EducationLevel
from project.schemas.authorization import authorizations
from project.schemas.education_levels import education_level_model, paginated_education_level_model
from project.schemas.pagination import pagination_parser, custom_schema_pagination


education_levels_ns = Namespace(
    name="test-jwt-education-levels", description="Education levels", authorizations=authorizations
)


@education_levels_ns.route("")
class EducationLevelsList(Resource):
    """Shows a list of all education levels, and lets you POST to add new education level"""
    method_decorators = [jwt_required()]

    @education_levels_ns.doc(security="jsonWebToken")
    @education_levels_ns.expect(pagination_parser)
    @education_levels_ns.marshal_with(paginated_education_level_model)
    def get(self):
        """List all education levels"""
        return pagination.paginate(
            EducationLevel, education_level_model, pagination_schema_hook=custom_schema_pagination
        )

    @education_levels_ns.expect(education_level_model, pagination_parser)
    @education_levels_ns.marshal_with(paginated_education_level_model)
    def post(self):
        """Adds a new education level"""
        education_level = EducationLevel()
        for key, value in education_levels_ns.payload.items():
            setattr(education_level, key, value)
        db.session.add(education_level)
        db.session.commit()
        return pagination.paginate(
            EducationLevel, education_level_model, pagination_schema_hook=custom_schema_pagination
        )


def get_education_level_or_404(id):
    education_level = EducationLevel.query.get(id)
    if not education_level:
        abort(404, "Education level not found")
    return education_level


@education_levels_ns.route("/<int:id>")
@education_levels_ns.response(404, "Education level not found")
@education_levels_ns.param("id", "The education level's unique identifier")
class EducationLevelsDetail(Resource):
    """Show an education level and lets you delete and modify it"""

    @education_levels_ns.marshal_with(education_level_model)
    def get(self, id):
        """Fetch the education_level with a given id"""
        return get_education_level_or_404(id)

    @education_levels_ns.expect(education_level_model, pagination_parser, validate=False)
    @education_levels_ns.marshal_with(paginated_education_level_model)
    def patch(self, id):
        """Update the education level with a given id"""
        education_level = get_education_level_or_404(id)
        education_level_keys = education_level_model.keys()
        for key, value in education_levels_ns.payload.items():
            if key in education_level_keys:
                setattr(education_level, key, value)
        db.session.commit()
        return pagination.paginate(
            EducationLevel, education_level_model, pagination_schema_hook=custom_schema_pagination
        )

    @education_levels_ns.expect(pagination_parser)
    @education_levels_ns.marshal_with(paginated_education_level_model)
    def delete(self, id):
        """Delete the education level with a given id"""
        education_level = get_education_level_or_404(id)
        db.session.delete(education_level)
        db.session.commit()
        return pagination.paginate(
            EducationLevel, education_level_model, pagination_schema_hook=custom_schema_pagination
        )
