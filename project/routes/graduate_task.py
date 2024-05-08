from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import GraduateTask, Roles
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.authorization import authorizations
from project.schemas.graduate_task import (
    graduate_task_response_model,
    graduate_task_model,
)
from project.validators import allowed_roles, verify_teacher

graduate_tasks_ns = Namespace(
    "syllabuses/graduate-tasks",
    description="Graduate tasks",
    authorizations=authorizations,
)


def create_graduate_tasks(syllabus_id, tasks):

    for fields in tasks:
        graduate_task = GraduateTask(
            syllabus_id=syllabus_id,
            name=fields.get("name"),
            controls=fields.get("controls"),
            deadlines=fields.get("deadlines"),
        )
        db.session.add(graduate_task)

    db.session.commit()


def get_graduate_task_or_404(id):
    graduate_task = GraduateTask.query.get(id)
    if not graduate_task:
        abort(404, f"Graduate task with id {id} not found")
    return graduate_task


def get_graduate_task_response(syllabus_id):
    graduate_tasks = (
        db.session.query(GraduateTask).filter_by(syllabus_id=syllabus_id).all()
    )
    return {
        "graduate_tasks": graduate_tasks,
        "syllabus_id": syllabus_id,
    }


@graduate_tasks_ns.route("/<int:syllabus_id>")
@graduate_tasks_ns.param("syllabus_id", "The syllabus unique identifier")
class GraduateTasksList(Resource):
    """Get list of graduate tasks or create a new graduate task"""

    @graduate_tasks_ns.marshal_with(graduate_task_response_model, envelope="content")
    def get(self, syllabus_id):
        """Get list of graduate tasks by given syllabus_id"""
        return get_graduate_task_response(syllabus_id)

    @graduate_tasks_ns.expect(graduate_task_response_model)
    @graduate_tasks_ns.marshal_with(graduate_task_response_model, envelope="content")
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, syllabus_id):
        """Create a new graduate task"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        create_graduate_tasks(
            syllabus_id, graduate_tasks_ns.payload.get("graduate_tasks")
        )

        set_syllabus_filling_status(syllabus_id)

        return get_graduate_task_response(syllabus_id)


@graduate_tasks_ns.route("/<int:task_id>")
@graduate_tasks_ns.param("task_id", "The graduate task unique identifier")
class GraduateTaskDetail(Resource):
    """Show graduate tasks and lets you modify or delete it"""

    @graduate_tasks_ns.expect(graduate_task_model)
    @graduate_tasks_ns.marshal_with(graduate_task_response_model, envelope="content")
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
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

        set_syllabus_filling_status(syllabus.id)

        return get_graduate_task_response(syllabus.id)

    @graduate_tasks_ns.marshal_with(graduate_task_response_model, envelope="content")
    @graduate_tasks_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, task_id):
        """Delete the graduate task with a given id"""
        graduate_task = get_graduate_task_or_404(task_id)
        syllabus = graduate_task.syllabus
        verify_teacher(syllabus)

        db.session.delete(graduate_task)
        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_graduate_task_response(syllabus.id)
