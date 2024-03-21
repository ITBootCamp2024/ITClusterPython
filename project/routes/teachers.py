from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.schema import teacher_model
from project.models import Teacher


teachers_ns = Namespace(name="teachers", description="info about teachers")


@teachers_ns.route("/")
class TeachersList(Resource):
    """Shows a list of all teachers, and lets you POST to add new teacher"""

    @teachers_ns.marshal_list_with(teacher_model)
    def get(self):
        """List all teachers"""
        return Teacher.query.all()

    @teachers_ns.expect(teacher_model)
    @teachers_ns.marshal_list_with(teacher_model)
    def post(self):
        """Adds a new teacher"""
        teacher = Teacher(
            name=teachers_ns.payload["name"],
            role=teachers_ns.payload["role"],
            status=teachers_ns.payload["status"],
            email=teachers_ns.payload["email"],
            details=teachers_ns.payload["details"],
        )
        db.session.add(teacher)
        db.session.commit()
        return teacher, 201


def get_teacher_or_404(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        abort(404, "Teacher not found")
    return teacher


@teachers_ns.route("/<int:id>/")
@teachers_ns.response(404, "Teacher not found")
@teachers_ns.param("id", "The teacher's unique identifier")
class TeachersDetail(Resource):
    """Show a teacher and lets you delete him"""

    @teachers_ns.marshal_with(teacher_model)
    def get(self, id):
        """Fetch the teacher with a given id"""
        return get_teacher_or_404(id)

    @teachers_ns.expect(teacher_model)
    @teachers_ns.marshal_list_with(teacher_model)
    def put(self, id):
        """Update the teacher with a given id"""
        teacher = get_teacher_or_404(id)
        teacher.name = teachers_ns.payload["name"]
        teacher.role = teachers_ns.payload["role"]
        teacher.status = teachers_ns.payload["status"]
        teacher.email = teachers_ns.payload["email"]
        teacher.details = teachers_ns.payload["details"]
        db.session.commit()
        return teacher

    def delete(self, id):
        """Delete the teacher with a given id"""
        teacher = get_teacher_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        return {}, 204
