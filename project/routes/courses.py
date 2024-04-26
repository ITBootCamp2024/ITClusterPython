from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, Namespace, abort
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from project.models import Discipline, Teacher, Roles
from project.extensions import db
from project.schemas.authorization import authorizations
from project.schemas.service_info import serviced_course_model
from project.validators import allowed_roles

courses_ns = Namespace(name="courses",
                       description="Courses information",
                       authorizations=authorizations)


def get_courses(teacher_id: int):
    """Get list of courses"""
    disciplines = db.session.query(Discipline) \
        .options(joinedload(Discipline.syllabus)) \
        .filter_by(teacher_id=teacher_id) \
        .order_by(desc("id")).all()
    result = []
    for discipline in disciplines:
        syllabus = discipline.syllabus
        if not syllabus:
            continue
        result.append({
            "teacher_id": teacher_id,
            "discipline": {
                "id": discipline.id,
                "name": discipline.name
            },
            "syllabus": {
                "id": syllabus.id,
                "name": syllabus.name,
                "status": syllabus.status
            }
        })
    return {
        "content": result,
        "totalElements": len(result)
    }


@courses_ns.route("/<int:teacher_id>")
class CoursesList(Resource):
    """Shows a list of all courses of a given teacher"""

    @courses_ns.marshal_with(serviced_course_model)
    def get(self, teacher_id):
        """Get list of courses by given teacher_id"""
        return get_courses(teacher_id)


@courses_ns.route("/my")
class CoursesListMy(Resource):
    """Shows a list of all courses of a logged teacher"""
    @courses_ns.doc(security="jsonWebToken",
                    description="Shows all courses of the logged teacher")
    @courses_ns.response(400, "Teacher with email <email> does not exist")
    @courses_ns.marshal_with(serviced_course_model)
    @allowed_roles([Roles.TEACHER])
    def get(self):
        email = get_jwt_identity()
        teacher = Teacher.query.filter_by(email=email).first()

        if not teacher:
            abort(400, f"Teacher with email '{email}' does not exist")

        return get_courses(teacher.id)
