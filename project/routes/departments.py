from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.models import Department
from project.schemas.departments import paginated_department_model, department_model, department_query_model
from project.schemas.pagination import pagination_parser, custom_schema_pagination
from project.validators import validate_site

departments_ns = Namespace(name="department", description="info about departments")


@departments_ns.route("")
class DepartmentsList(Resource):
    """Shows a list of all departments, and lets you POST to add new department"""

    @departments_ns.expect(pagination_parser)
    @departments_ns.marshal_with(paginated_department_model)
    def get(self):
        """List all departments"""
        return pagination.paginate(
            Department, department_model, pagination_schema_hook=custom_schema_pagination
        )

    @departments_ns.expect(department_query_model, pagination_parser)
    @departments_ns.marshal_with(paginated_department_model)
    @validate_site('http', ["url"])
    def post(self):
        """Adds a new department"""
        department = Department()
        plain_params = ["name", "description", "url"]
        nested_ids = ["university"]
        for key, value in departments_ns.payload.items():
            if key in plain_params:
                setattr(department, key, value)
            elif key in nested_ids:
                setattr(department, key + "_id", value.get("id"))
        department.contacts = departments_ns.payload.get("contacts")
        db.session.add(department)
        db.session.commit()
        return pagination.paginate(
            Department, department_model, pagination_schema_hook=custom_schema_pagination
        )


def get_department_or_404(id):
    department = Department.query.get(id)
    if not department:
        abort(404, "Department not found")
    return department


@departments_ns.route("/<int:id>")
@departments_ns.response(404, "Department not found")
@departments_ns.param("id", "The department's unique identifier")
class DepartmentDetail(Resource):
    """Show a department and lets you delete it"""

    @departments_ns.marshal_with(department_model)
    def get(self, id):
        """Fetch the department with a given id"""
        return get_department_or_404(id)

    @departments_ns.expect(department_query_model, pagination_parser, validate=False)
    @departments_ns.marshal_with(paginated_department_model)
    @validate_site('http', ["url"])
    def patch(self, id):
        """Update the department with a given id"""
        department = get_department_or_404(id)
        plain_params = ["name", "description", "url"]
        nested_ids = ["university"]
        for key, value in departments_ns.payload.items():
            if key in plain_params:
                setattr(department, key, value)
            elif key in nested_ids:
                setattr(department, key + "_id", value.get("id"))
        department.contacts = departments_ns.payload.get("contacts")
        db.session.commit()
        return pagination.paginate(
            Department, department_model, pagination_schema_hook=custom_schema_pagination
        )

    @departments_ns.expect(pagination_parser)
    @departments_ns.marshal_with(paginated_department_model)
    def delete(self, id):
        """Delete the department with given id"""
        department = get_department_or_404(id)
        db.session.delete(department)
        db.session.commit()
        return pagination.paginate(
            Department, department_model, pagination_schema_hook=custom_schema_pagination
        )
