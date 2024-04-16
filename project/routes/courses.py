from typing import Optional

from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, Namespace, abort

from project import Teacher
from project.extensions import db
from project.schemas.authorization import authorizations
from project.schemas.courses import teacher_id_parser
from project.schemas.service_info import serviced_course_model, serviced_course_with_name_model
from project.validators import allowed_roles

courses_ns = Namespace(name="courses",
                       description="Courses information",
                       authorizations=authorizations)


def get_courses(teacher_id: Optional[int] = None):
    """Get list of courses"""
    teachers = db.session.query(Teacher)
    if teacher_id:
        teachers = teachers.filter_by(id=teacher_id)
    teachers = teachers.all()
    print([teacher.name for teacher in teachers])
    result = []
    for teacher in teachers:
        print(f"{teacher.name=}")
        for discipline in teacher.disciplines:
            print(f"{discipline.name=}")
            for syllabus in discipline.syllabuses:
                print(f"{syllabus.name=}")
                result.append({
                    "id": teacher.id,
                    "name": teacher.name,
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
    print(result)
    return {
        "content": result,
        "totalElements": len(result)
    }


@courses_ns.route("")
class CoursesList(Resource):
    """Shows a list of all courses or courses of a given teacher"""

    @courses_ns.expect(teacher_id_parser)
    @courses_ns.marshal_with(serviced_course_with_name_model)
    def get(self):
        """Get list of courses by given teacher_id"""
        args = teacher_id_parser.parse_args()
        teacher_id = args.get("teacher_id")
        return get_courses(teacher_id)


@courses_ns.route("/my")
class CoursesListMy(Resource):
    """Shows a list of all courses of a logged teacher"""
    @courses_ns.doc(security="jsonWebToken",
                    description="Shows all courses of the logged teacher")
    @courses_ns.marshal_with(serviced_course_model)
    @allowed_roles(["teacher"])
    def get(self):
        email = get_jwt_identity()
        teacher = Teacher.query.filter_by(email=email).first()

        if not teacher:
            abort(400, f"Teacher with email '{email}' does not exist")

        return get_courses(teacher.id)
