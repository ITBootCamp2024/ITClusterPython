from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model

assessment_model = api.model(
    "AssessmentSchema",
    {
        "id": fields.Integer(
            readonly=True, description="Unique identifier of the assessment", default=1
        ),
        "object": fields.String(
            required=True,
            max_length=255,
            description="object of the assessment",
        ),
        "method": fields.String(
            required=True,
            max_length=255,
            description="assessment method",
        ),
        "tool": fields.String(
            required=True,
            max_length=255,
            description="assessment tool",
        ),
    },
)


assessment_response_model = api.model(
    "AssessmentResponse",
    {
        "assessments": fields.List(
            fields.Nested(assessment_model), required=True
        ),
        **syllabus_id_model
    },
)
