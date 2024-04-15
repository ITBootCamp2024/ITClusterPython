from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Teacher, Position, University, Role
from project.schemas.service_info import serviced_teacher_model
from project.schemas.teachers import teacher_model, teacher_query_model

teachers_ns = Namespace(name="teachers", description="info about teachers")


def get_teacher_or_404(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        abort(404, "Teacher not found")
    return teacher


def get_teacher_response():
    teachers = Teacher.query.all()
    positions = Position.query.all()
    university = University.query.all()

    return {
        "content": teachers,
        "service_info": {
            "position": positions,
            "university": university
        },
        "totalElements": len(teachers)
    }


@teachers_ns.route("")
class TeachersList(Resource):
    """Shows a list of all teachers, and lets you POST to add new teacher"""

    @teachers_ns.marshal_with(serviced_teacher_model)
    def get(self):
        """List all teachers"""
        return get_teacher_response()

    @teachers_ns.expect(teacher_query_model)
    @teachers_ns.marshal_with(serviced_teacher_model)
    def post(self):
        """Adds a new teacher"""
        teacher = Teacher()
        plain_params = ["name", "email", "degree_level", "comments"]
        nested_ids = ["position", "department"]
        for key, value in teachers_ns.payload.items():
            if key in plain_params:
                setattr(teacher, key, value)
            elif key in nested_ids:
                setattr(teacher, key + "_id", value.get("id"))
        teacher.role_id = Role.query.filter_by(name="teacher").first().id
        db.session.add(teacher)
        db.session.commit()
        return get_teacher_response()


@teachers_ns.route("/<int:id>")
@teachers_ns.response(404, "Teacher not found")
@teachers_ns.param("id", "The teacher's unique identifier")
class TeachersDetail(Resource):
    """Show a teacher and lets you delete him"""

    @teachers_ns.marshal_with(teacher_model)
    def get(self, id):
        """Fetch the teacher with a given id"""
        return get_teacher_or_404(id)

    @teachers_ns.expect(teacher_query_model, validate=False)
    @teachers_ns.marshal_with(serviced_teacher_model)
    def patch(self, id):
        """Update the teacher with a given id"""
        teacher = get_teacher_or_404(id)
        plain_params = ["name", "email", "degree_level", "comments"]
        nested_ids = ["position", "department"]
        for key, value in teachers_ns.payload.items():
            if key in plain_params:
                setattr(teacher, key, value)
            elif key in nested_ids:
                setattr(teacher, key + "_id", value.get("id"))
        db.session.commit()
        return get_teacher_response()

    @teachers_ns.marshal_with(serviced_teacher_model)
    def delete(self, id):
        """Delete the teacher with given id"""
        teacher = get_teacher_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        return get_teacher_response()
