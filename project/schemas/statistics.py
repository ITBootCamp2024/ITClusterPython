from flask_restx import fields

from project.extensions import api


user_type_statistics_model = api.model(
    "UserTypeStatistics",
    {
        "registered": fields.Integer(),
        "verified": fields.Integer(),
    },
)

user_statistics_model = api.model(
    "UserStatistics",
    {
        "teachers": fields.Nested(user_type_statistics_model),
        "experts": fields.Nested(user_type_statistics_model),
        "students": fields.Nested(user_type_statistics_model),
    },
)

syllabus_statistics_model = api.model(
    "SyllabusStatistics",
    {
        "total_syllabuses": fields.Integer(),
        "on_filling": fields.Integer(),
        "filled": fields.Integer(),
        "proposed": fields.Integer(),
        "accepted": fields.Integer(),
        "reviewed": fields.Integer(),
        "negative": fields.Integer(),
        "conditionally_negative": fields.Integer(),
        "conditionally_positive": fields.Integer(),
        "positive": fields.Integer(),
    }
)
