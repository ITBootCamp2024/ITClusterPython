from flask_restx import fields

from project.extensions import api


assessment_model = api.model(
    "AssessmentSchema",
    {
        "id": fields.Integer(
            readonly=True, description="Unique identifier of the assessment", default=1
        ),
        "syllabus_id": fields.Integer(
            required=True, description="Unique identifier of the syllabus", default=1
        ),
        "object": fields.String(
            required=True,
            max_length=255,
            default="object of the assessment",
        ),
        "method": fields.String(
            required=True,
            max_length=255,
        ),
        "tool": fields.String(
            required=True,
            max_length=255,
        ),
    },
)
