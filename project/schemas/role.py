from flask_restx import fields

from project.extensions import api


role_model = api.model(
    "Role",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the role",
            default=1
        ),
        "name": fields.String(
            required=True,
            description="The role name",
            max_length=45,
            default="role"
        )
    }
)
