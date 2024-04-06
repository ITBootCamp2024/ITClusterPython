from flask_restx import fields

from project.extensions import api
from project.schemas.general import base_id_model
from project.schemas.pagination import get_pagination_schema_for
from project.schemas.universities import short_university_model


contacts_model = api.model(
    "Contacts",
    {
        "address": fields.String(
            required=True,
            description="department address",
            max_length=255,
            default="address"
        ),
        "email": fields.String(
            required=True,
            description="email of the department",
            max_length=45,
            default="email@email.com"
        ),
        "phone": fields.List(
            fields.String(
                required=True,
                description="phone number of the department",
                max_length=45,
                default="+00(000)000-00-00"
            ),
            required=True
        )
    }
)


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
            min_length=2,
            max_length=100,
            default="name"
        ),
    }
)


short_department_model_with_url = api.model(
    "ShortDepartmentWithUrl",
    {
        **short_department_model,
        "url": fields.String(
            required=True,
            description="link to the department",
            max_length=255,
            default="http://example.com"
        )
    }
)


base_department_model = api.model(
    "BaseDepartment",
    {
        **short_department_model_with_url,
        **contacts_model,
        "description": fields.String(
            required=True,
            description="description of the department",
            default="department description"
        ),
    }
)


department_model = api.model(
    "Department",
    {
        **base_department_model,
        "university": fields.Nested(short_university_model, required=True),
    }
)


department_query_model = api.model(
    "DepartmentQuery",
    {
        **base_department_model,
        "university": fields.Nested(base_id_model, required=True)
    }
)


paginated_department_model = get_pagination_schema_for(department_model)
