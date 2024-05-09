from flask_restx import Resource, Namespace

from project import Teacher
from project.models import Specialist
from project.schemas.statistics import user_statistics_model, syllabus_statistics_model

statistics_ns = Namespace(name="statistics", description="statistics information")


@statistics_ns.route("/users")
class StatisticsUsers(Resource):

    @statistics_ns.marshal_with(user_statistics_model)
    def get(self):
        """Show users statistics"""

        total_teachers = Teacher.query.count()
        verified_teachers = Teacher.query.filter_by(verified=True).count()

        total_experts = Specialist.query.count()
        verified_experts = Specialist.query.filter_by(verified=True).count()

        # TODO: add students statistics
        total_students = 5
        verified_students = 3

        return {
            "teachers": {
                "registered": total_teachers,
                "verified": verified_teachers,
            },
            "experts": {
                "registered": total_experts,
                "verified": verified_experts,
            },
            "students": {
                "registered": total_students,
                "verified": verified_students,
            },
        }


@statistics_ns.route("/syllabuses")
class StatisticsSyllabuses(Resource):

    @statistics_ns.marshal_with(syllabus_statistics_model)
    def get(self):
        """Show syllabuses statistics"""

        return {
            "total_syllabuses": 0,
            "on_filling": 0,
            "filled": 0,
            "proposed": 0,
            "accepted": 0,
            "reviewed": 0,
            "negative": 0,
            "conditionally_negative": 0,
            "conditionally_positive": 0,
            "positive": 0,
        }
