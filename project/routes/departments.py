from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Department, University, Roles
from project.schemas.authorization import authorizations
from project.schemas.departments import (
    department_model,
    department_query_model,
    contacts_model,
)
from project.schemas.service_info import serviced_department_model
from project.validators import validate_site, allowed_roles

departments_ns = Namespace(
    name="department",
    description="info about departments",
    authorizations=authorizations,
)


def get_department_or_404(id):
    department = Department.query.get(id)
    department.phone = department.phone.split(", ")
    if not department:
        abort(404, "Department not found")
    return department


def get_department_response():
    departments = Department.query.all()
    for department in departments:
        department.phone = department.phone.split(", ")
    universities = University.query.all()
    return {
        "content": departments,
        "service_info": {
            "university": universities,
        },
        "totalElements": len(departments),
    }


@departments_ns.route("")
class DepartmentsList(Resource):
    """Shows a list of all departments, and lets you POST to add new department"""

    @departments_ns.marshal_with(serviced_department_model)
    def get(self):
        """List all departments"""
        return get_department_response()

    @departments_ns.expect(department_query_model)
    @departments_ns.marshal_with(serviced_department_model)
    @validate_site("http", ["url"])
    @departments_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
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
        department.contacts = {
            key: departments_ns.payload.get(key) for key in contacts_model.keys()
        }
        db.session.add(department)
        db.session.commit()
        return get_department_response()


@departments_ns.route("/<int:id>")
@departments_ns.response(404, "Department not found")
@departments_ns.param("id", "The department's unique identifier")
class DepartmentDetail(Resource):
    """Show a department and lets you delete it"""

    @departments_ns.marshal_with(department_model)
    def get(self, id):
        """Fetch the department with a given id"""
        return get_department_or_404(id)

    @departments_ns.expect(department_query_model, validate=False)
    @departments_ns.marshal_with(serviced_department_model)
    @validate_site("http", ["url"])
    @departments_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
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
        department.contacts = {
            key: departments_ns.payload.get(key) for key in contacts_model.keys()
        }
        db.session.commit()
        return get_department_response()

    @departments_ns.marshal_with(serviced_department_model)
    @departments_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, id):
        """Delete the department with given id"""
        department = get_department_or_404(id)
        db.session.delete(department)
        db.session.commit()
        return get_department_response()
