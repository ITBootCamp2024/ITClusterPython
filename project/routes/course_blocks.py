from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.schema import (
    course_blocks_model,
    pagination_parser,
    custom_schema_pagination,
)
from project.models import CourseBlocks

course_blocks_ns = Namespace(
    name="course_blocks", description="Courses and their descriptions"
)


@course_blocks_ns.route("")
@course_blocks_ns.response(200, model=[course_blocks_model], description="Success")
class CourseBlocksList(Resource):
    """Shows a list of all courses, and lets you POST to add new courses"""

    @course_blocks_ns.expect(pagination_parser)
    def get(self):
        """List all courses"""
        return pagination.paginate(
            CourseBlocks,
            course_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_blocks_ns.expect(course_blocks_model, pagination_parser)
    def post(self):
        """Create a new courses"""
        course = CourseBlocks(
            name=course_blocks_ns.payload["name"],
            description=course_blocks_ns.payload["description"],
        )
        db.session.add(course)
        db.session.commit()
        return pagination.paginate(
            CourseBlocks,
            course_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )


def get_course_or_404(id):
    course = CourseBlocks.query.get(id)
    if not course:
        abort(404, "Course not found")
    return course


@course_blocks_ns.route("/<int:id>")
@course_blocks_ns.response(200, model=[course_blocks_model], description="Success")
@course_blocks_ns.response(404, "Course not found")
@course_blocks_ns.param("id", "The course unique identifier")
class CourseBlocksDetail(Resource):
    """Show a single course and lets you delete them"""

    @course_blocks_ns.marshal_with(course_blocks_model)
    def get(self, id):
        """Fetch a given course"""
        return get_course_or_404(id)

    @course_blocks_ns.expect(course_blocks_model, pagination_parser)
    def put(self, id):
        """Update a course given its identifier"""
        course = get_course_or_404(id)
        course.name = course_blocks_ns.payload["name"]
        course.description = course_blocks_ns.payload["description"]
        db.session.commit()
        return pagination.paginate(
            CourseBlocks,
            course_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_blocks_ns.expect(pagination_parser)
    def delete(self, id):
        """Delete a course given its identifier"""
        course = get_course_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return pagination.paginate(
            CourseBlocks,
            course_blocks_model,
            pagination_schema_hook=custom_schema_pagination,
        )
