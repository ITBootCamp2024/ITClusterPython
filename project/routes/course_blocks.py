from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.schema import course_blocks_model
from project.models import CourseBlocks

course_blocks = Namespace(
    name="course_blocks", description="Courses and their descriptions"
)


@course_blocks.route("/")
class CourseBlocksList(Resource):
    """Shows a list of all courses, and lets you POST to add new courses"""

    @course_blocks.marshal_list_with(course_blocks_model)
    def get(self):
        """List all courses"""
        return CourseBlocks.query.all()

    @course_blocks.expect(course_blocks_model)
    @course_blocks.marshal_list_with(course_blocks_model)
    def post(self):
        """Create a new courses"""
        course = CourseBlocks(
            name=course_blocks.payload["name"],
            description=course_blocks.payload["description"],
        )
        db.session.add(course)
        db.session.commit()
        return course, 201


def get_course_or_404(id):
    course = CourseBlocks.query.get(id)
    if not course:
        abort(404, "Course not found")
    return course


@course_blocks.route("/<int:id>/")
@course_blocks.response(404, "Course not found")
@course_blocks.param("id", "The course unique identifier")
class CourseBlocksDetail(Resource):
    """Show a single course and lets you delete them"""

    @course_blocks.marshal_with(course_blocks_model)
    def get(self, id):
        """Fetch a given course"""
        return get_course_or_404(id)

    @course_blocks.expect(course_blocks_model)
    @course_blocks.marshal_list_with(course_blocks_model)
    def put(self, id):
        """Update a course given its identifier"""
        course = get_course_or_404(id)
        course.name = course_blocks.payload["name"]
        course.description = course_blocks.payload["description"]
        db.session.commit()
        return course

    def delete(self, id):
        """Delete a course given its identifier"""
        course = get_course_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204
