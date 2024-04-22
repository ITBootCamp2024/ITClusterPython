from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import GraduateTask
from project.routes.syllabus import get_syllabus_or_404, verify_teacher
from project.schemas.authorization import authorizations
from project.schemas.graduate_task import graduate_task_response_model, graduate_task_model
from project.validators import allowed_roles

graduate_tasks_ns = Namespace(
    "syllabuses/graduate-tasks",
    description="Graduate tasks",
    authorizations=authorizations
)


def get_graduate_task_or_404(id):
    graduate_task = GraduateTask.query.get(id)
    if not graduate_task:
        abort(404, f"Graduate task with id {id} not found")
    return graduate_task


def get_graduate_task_response(syllabus_id):
    graduate_tasks = db.session.query(GraduateTask).filter_by(syllabus_id=syllabus_id).all()
    return {
        "graduate_tasks": graduate_tasks,
        "syllabus_id": syllabus_id,
    }


@graduate_tasks_ns.route("/<int:syllabus_id>")
@graduate_tasks_ns.param("syllabus_id", "The syllabus unique identifier")
class GraduateTasksList(Resource):
    """Get list of graduate tasks or create a new graduate task"""
    @graduate_tasks_ns.marshal_with(graduate_task_response_model)
    def get(self, syllabus_id):
        """Get list of graduate tasks by given syllabus_id"""
        return get_graduate_task_response(syllabus_id)

    @graduate_tasks_ns.expect(graduate_task_model)
    @graduate_tasks_ns.marshal_with(graduate_task_response_model)
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def post(self, syllabus_id):
        """Create a new graduate task"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        graduate_task = GraduateTask(
            syllabus_id=syllabus_id,
            name=graduate_tasks_ns.payload.get("name"),
            controls=graduate_tasks_ns.payload.get("controls"),
            deadlines=graduate_tasks_ns.payload.get("deadlines"),
        )
        db.session.add(graduate_task)
        db.session.commit()

        return get_graduate_task_response(syllabus_id)


@graduate_tasks_ns.route("/<int:task_id>")
@graduate_tasks_ns.param("task_id", "The graduate task unique identifier")
class GraduateTaskDetail(Resource):
    """Show graduate tasks and lets you modify or delete it"""

    @graduate_tasks_ns.expect(graduate_task_model)
    @graduate_tasks_ns.marshal_with(graduate_task_response_model)
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def patch(self, task_id):
        """Update the graduate task with a given id"""
        graduate_task = get_graduate_task_or_404(task_id)
        syllabus = graduate_task.syllabus
        verify_teacher(syllabus)

        plain_params = ["name", "controls", "deadlines"]
        for key, value in graduate_tasks_ns.payload.items():
            if key in plain_params:
                setattr(graduate_task, key, value)

        db.session.commit()
        return get_graduate_task_response(syllabus.id)

    @graduate_tasks_ns.marshal_with(graduate_task_response_model)
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def delete(self, task_id):
        """Delete the graduate task with a given id"""
        graduate_task = get_graduate_task_or_404(task_id)
        syllabus = graduate_task.syllabus
        verify_teacher(syllabus)

        db.session.delete(graduate_task)
        db.session.commit()
        return get_graduate_task_response(syllabus.id)
