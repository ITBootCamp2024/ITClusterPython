from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import EducationLevel, Roles
from project.schemas.authorization import authorizations
from project.schemas.education_levels import education_level_model
from project.schemas.service_info import serviced_education_level_model
from project.validators import allowed_roles

education_levels_ns = Namespace(
    name="education-levels",
    description="Education levels",
    authorizations=authorizations,
)


def get_education_level_or_404(id):
    education_level = EducationLevel.query.get(id)
    if not education_level:
        abort(404, "Education level not found")
    return education_level


def get_education_level_response():
    education_levels = EducationLevel.query.all()
    return {"content": education_levels, "totalElements": len(education_levels)}


@education_levels_ns.route("")
class EducationLevelsList(Resource):
    """Shows a list of all education levels, and lets you POST to add new education level"""

    @education_levels_ns.marshal_with(serviced_education_level_model)
    def get(self):
        """List all education levels"""
        return get_education_level_response()

    @education_levels_ns.expect(education_level_model)
    @education_levels_ns.marshal_with(serviced_education_level_model)
    @education_levels_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self):
        """Adds a new education level"""
        education_level = EducationLevel()
        for key, value in education_levels_ns.payload.items():
            setattr(education_level, key, value)
        db.session.add(education_level)
        db.session.commit()
        return get_education_level_response()


@education_levels_ns.route("/<int:id>")
@education_levels_ns.response(404, "Education level not found")
@education_levels_ns.param("id", "The education level's unique identifier")
class EducationLevelsDetail(Resource):
    """Show an education level and lets you delete and modify it"""

    @education_levels_ns.marshal_with(education_level_model)
    def get(self, id):
        """Fetch the education_level with a given id"""
        return get_education_level_or_404(id)

    @education_levels_ns.expect(education_level_model, validate=False)
    @education_levels_ns.marshal_with(serviced_education_level_model)
    @education_levels_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, id):
        """Update the education level with a given id"""
        education_level = get_education_level_or_404(id)
        education_level_keys = education_level_model.keys()
        for key, value in education_levels_ns.payload.items():
            if key in education_level_keys:
                setattr(education_level, key, value)
        db.session.commit()
        return get_education_level_response()

    @education_levels_ns.marshal_with(serviced_education_level_model)
    @education_levels_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete the education level with a given id"""
        education_level = get_education_level_or_404(id)
        db.session.delete(education_level)
        db.session.commit()
        return get_education_level_response()
