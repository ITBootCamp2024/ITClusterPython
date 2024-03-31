from flask_restx import Resource, Namespace, abort
from sqlalchemy.exc import IntegrityError

from project.extensions import db, pagination
from project.models import Teacher
from project.schema import (
    teacher_model,
    teacher_query_model,
    pagination_parser,
    custom_schema_pagination,
    paginated_teacher_model,
)


teachers_ns = Namespace(name="teachers", description="info about teachers")


@teachers_ns.route("")
class TeachersList(Resource):
    """Shows a list of all teachers, and lets you POST to add new teacher"""

    @teachers_ns.expect(pagination_parser)
    @teachers_ns.marshal_with(paginated_teacher_model)
    def get(self):
        """List all teachers"""
        return pagination.paginate(
            Teacher, teacher_model, pagination_schema_hook=custom_schema_pagination
        )

    @teachers_ns.response(400, "Email should be unique")
    @teachers_ns.expect(teacher_query_model, pagination_parser)
    @teachers_ns.marshal_with(paginated_teacher_model)
    def post(self):
        """Adds a new teacher"""
        teacher = Teacher()
        plain_params = ["name", "email", "comments"]
        nested_ids = ["position", "degree", "department"]
        for key, value in teachers_ns.payload.items():
            if key in plain_params:
                setattr(teacher, key, value)
            elif key in nested_ids:
                setattr(teacher, key + "_id", value.get("id"))
        try:
            db.session.add(teacher)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "Email should be unique")
        return pagination.paginate(
            Teacher, teacher_model, pagination_schema_hook=custom_schema_pagination
        )


def get_teacher_or_404(id):
    teacher = Teacher.query.get(id)
    if not teacher:
        abort(404, "Teacher not found")
    return teacher


@teachers_ns.route("/<int:id>")
@teachers_ns.response(404, "Teacher not found")
@teachers_ns.param("id", "The teacher's unique identifier")
class TeachersDetail(Resource):
    """Show a teacher and lets you delete him"""

    @teachers_ns.marshal_with(teacher_model)
    def get(self, id):
        """Fetch the teacher with a given id"""
        return get_teacher_or_404(id)

    @teachers_ns.response(400, "Email should be unique")
    @teachers_ns.expect(teacher_query_model, pagination_parser, validate=False)
    @teachers_ns.marshal_with(paginated_teacher_model)
    def patch(self, id):
        """Update the teacher with a given id"""
        teacher = get_teacher_or_404(id)
        plain_params = ["name", "email", "comments"]
        nested_ids = ["position", "degree", "department"]
        for key, value in teachers_ns.payload.items():
            if key in plain_params:
                setattr(teacher, key, value)
            elif key in nested_ids:
                setattr(teacher, key + "_id", value.get("id"))
        db.session.commit()
        return pagination.paginate(
            Teacher, teacher_model, pagination_schema_hook=custom_schema_pagination
        )

    @teachers_ns.expect(pagination_parser)
    @teachers_ns.marshal_with(paginated_teacher_model)
    def delete(self, id):
        """Delete the teacher with given id"""
        teacher = get_teacher_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        return pagination.paginate(
            Teacher, teacher_model, pagination_schema_hook=custom_schema_pagination
        )
