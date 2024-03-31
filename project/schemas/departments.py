from flask_restx import fields

from project.extensions import api


short_department_model = api.model(
    "ShortDepartment",
    {
        "id": fields.Integer(
            readonly=True,
            description="The unique identifier of the department",
        ),
        "name": fields.String(
            required=True,
            description="Name of the department",
            min_length=3,
            max_length=100,),
    }
)

department_model = api.model(
    "school",
    {
        "id": fields.Integer(
            readonly=True, description="School ID"
        ),
        "name": fields.String(description="School name"),
        "university_id": fields.Integer(description="Related University ID",
                                        min_length=1),
        "description": fields.String(required=False, description="Brief description",
                                     min_length=20, max_length=400,),
        "url": fields.String(required=False,  description="School site",
                              min_length=10, max_length=100,),
        "contact": fields.String(required=False, description="School contacts",
                                 min_length=5, max_length=100,),
    },
)
