from flask_restx import fields

from project.extensions import api
from project.schemas.disciplines import short_discipline_model

short_syllabus_model = api.model(
    "ShortSyllabus",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the syllabus",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="Syllabus name",
            max_length=255,
            default="syllabus name"
        )
    }
)


base_syllabus_model = api.model(
    "BaseSyllabus",
    {
        **short_syllabus_model,
        "status": fields.String(
            required=True,
            description="Status of the syllabus",
            max_length=45,
        )
    }
)


syllabus_model = api.model(
    "Syllabus",
    {
        **base_syllabus_model,
        "discipline": fields.Nested(short_discipline_model, required=True)
    }
)
