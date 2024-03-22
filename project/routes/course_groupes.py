from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.schema import (
    course_groupes_model,
    pagination_parser,
    custom_schema_pagination,
)
from project.models import CourseGroupes

course_groupes_ns = Namespace(name="course_groupes", description="Course_groupes")


@course_groupes_ns.route("/")
@course_groupes_ns.response(200, model=[course_groupes_model], description="Success")
class CourseGroupesList(Resource):
    """Shows a list of all course_groupes, and lets you POST to add new program level"""

    @course_groupes_ns.expect(pagination_parser)
    def get(self):
        """List all course_groupes levels"""
        return pagination.paginate(
            CourseGroupes,
            course_groupes_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_groupes_ns.expect(course_groupes_model, pagination_parser)
    def post(self):
        """Create a new course_groupes"""
        course_gp = CourseGroupes(
            name=course_groupes_ns.payload["name"],
            description=course_groupes_ns.payload["description"],
            type_id=course_groupes_ns.payload["type_id"],
        )
        db.session.add(course_gp)
        db.session.commit()
        return pagination.paginate(
            CourseGroupes,
            course_groupes_model,
            pagination_schema_hook=custom_schema_pagination,
        )


def get_course_groupes_or_404(id):
    course_gp = CourseGroupes.query.get(id)
    if not course_gp:
        abort(404, "The course group not found")
    return course_gp


@course_groupes_ns.route("/<int:id>/")
@course_groupes_ns.response(200, model=[course_groupes_model], description="Success")
@course_groupes_ns.response(404, "The course group not found")
@course_groupes_ns.param("id", "The course group unique identifier")
class ProgramLevelDetail(Resource):
    """Show a single course group and lets you delete them"""

    @course_groupes_ns.marshal_with(course_groupes_model)
    def get(self, id):
        """Fetch a given course group"""
        return get_course_groupes_or_404(id)

    @course_groupes_ns.expect(course_groupes_model, pagination_parser)
    def put(self, id):
        """Update a course group given its identifier"""
        course_gp = get_course_groupes_or_404(id)
        course_gp.name = course_groupes_ns.payload["name"]
        course_gp.description = course_groupes_ns.payload["description"]
        course_gp.type_id = course_groupes_ns.payload["type_id"]
        db.session.commit()
        return pagination.paginate(
            CourseGroupes,
            course_groupes_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_groupes_ns.expect(pagination_parser)
    def delete(self, id):
        """Delete a course group given its identifier"""
        course_gp = get_course_groupes_or_404(id)
        db.session.delete(course_gp)
        db.session.commit()
        return pagination.paginate(
            CourseGroupes,
            course_groupes_model,
            pagination_schema_hook=custom_schema_pagination,
        )
