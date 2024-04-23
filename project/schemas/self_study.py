from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model

self_study_topic_model = api.model(
    "SelfStudyTopic",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the self study topic",
            default=1,
        ),
        "name": fields.String(
            required=True,
            description="Self study topic name",
            default="self study topic name",
        ),
        "controls": fields.String(description="Self study topic controls"),
        "hours": fields.Integer(description="Self study topic hours"),
    },
)

self_study_topic_response_model = api.model(
    "SelfStudyTopicResponse",
    {
        "self_study_topics": fields.List(
            fields.Nested(self_study_topic_model), required=True
        ),
        **syllabus_id_model,
    },
)
