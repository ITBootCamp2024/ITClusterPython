from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.schema import (
    course_statuses_model,
    pagination_parser,
    custom_schema_pagination,
)
from project.models import CourseStatuses

course_statuses_ns = Namespace(
    name="course_statuses", description="Statuses and their descriptions"
)


@course_statuses_ns.route("/")
@course_statuses_ns.response(200, model=[course_statuses_model], description="Success")
class CourseStatusesList(Resource):
    """Shows a list of all statuses, and lets you POST to add new status"""

    @course_statuses_ns.expect(pagination_parser)
    def get(self):
        """List all statuses"""
        return pagination.paginate(
            CourseStatuses,
            course_statuses_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_statuses_ns.expect(course_statuses_model, pagination_parser)
    def post(self):
        """Create a new status"""
        status = CourseStatuses(
            name=course_statuses_ns.payload["name"],
            description=course_statuses_ns.payload["description"],
        )
        db.session.add(status)
        db.session.commit()
        return pagination.paginate(
            CourseStatuses,
            course_statuses_model,
            pagination_schema_hook=custom_schema_pagination,
        )


def get_status_or_404(id):
    status = CourseStatuses.query.get(id)
    if not status:
        abort(404, "Status not found")
    return status


@course_statuses_ns.route("/<int:id>/")
@course_statuses_ns.response(200, model=[course_statuses_model], description="Success")
@course_statuses_ns.response(404, "Status not found")
@course_statuses_ns.param("id", "The status unique identifier")
class CourseStatusesDetail(Resource):
    """Show a single status and lets you delete them"""

    @course_statuses_ns.marshal_with(course_statuses_model)
    def get(self, id):
        """Fetch a given status"""
        return get_status_or_404(id)

    @course_statuses_ns.expect(course_statuses_model, pagination_parser)
    def put(self, id):
        """Update a status given its identifier"""
        status = get_status_or_404(id)
        status.name = course_statuses_ns.payload["name"]
        status.description = course_statuses_ns.payload["description"]
        db.session.commit()
        return pagination.paginate(
            CourseStatuses,
            course_statuses_model,
            pagination_schema_hook=custom_schema_pagination,
        )

    @course_statuses_ns.expect(pagination_parser)
    def delete(self, id):
        """Delete a status given its identifier"""
        status = get_status_or_404(id)
        db.session.delete(status)
        db.session.commit()
        return pagination.paginate(
            CourseStatuses,
            course_statuses_model,
            pagination_schema_hook=custom_schema_pagination,
        )
