from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.schema import course_statuses_model
from project.models import CourseStatuses

course_statuses_ns = Namespace(
    name="course_statuses", description="Statuses and their descriptions"
)


@course_statuses_ns.route("/")
class CourseStatusesList(Resource):
    """Shows a list of all statuses, and lets you POST to add new status"""

    @course_statuses_ns.marshal_list_with(course_statuses_model)
    def get(self):
        """List all statuses"""
        return CourseStatuses.query.all()

    @course_statuses_ns.expect(course_statuses_model)
    @course_statuses_ns.marshal_list_with(course_statuses_model)
    def post(self):
        """Create a new status"""
        status = CourseStatuses(
            name=course_statuses_ns.payload["name"],
            description=course_statuses_ns.payload["description"],
        )
        db.session.add(status)
        db.session.commit()
        return status, 201


def get_status_or_404(id):
    status = CourseStatuses.query.get(id)
    if not status:
        abort(404, "Status not found")
    return status


@course_statuses_ns.route("/<int:id>/")
@course_statuses_ns.response(404, "Status not found")
@course_statuses_ns.param("id", "The status unique identifier")
class CourseStatusesDetail(Resource):
    """Show a single status and lets you delete them"""

    @course_statuses_ns.marshal_with(course_statuses_model)
    def get(self, id):
        """Fetch a given status"""
        return get_status_or_404(id)

    @course_statuses_ns.expect(course_statuses_model)
    @course_statuses_ns.marshal_list_with(course_statuses_model)
    def put(self, id):
        """Update a status given its identifier"""
        status = get_status_or_404(id)
        status.name = course_statuses_ns.payload["name"]
        status.description = course_statuses_ns.payload["description"]
        db.session.commit()
        return status

    def delete(self, id):
        """Delete a status given its identifier"""
        status = get_status_or_404(id)
        db.session.delete(status)
        db.session.commit()
        return {}, 204
