from flask_restx import fields

from project.extensions import api


base_id_model = api.model(
    "BaseID",
    {
        "id": fields.Integer(description="The unique identifier", required=True, default=1),
    }
)


base_name_model = api.model(
    "BaseName",
    {
        "name": fields.String(
            required=True,
            description="The name of the object",
            default="Some name",
        )
    }
)


syllabus_id_model = api.model(
    "SyllabusID",
    {
        "syllabus_id": fields.Integer(
            readonly=True, description="Unique identifier of the syllabus", default=1
        ),
    }
)
