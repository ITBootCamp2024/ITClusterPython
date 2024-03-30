from flask_restx import Resource, Namespace, abort

from project.extensions import db, pagination
from project.models import Degree
from project.schema import (
    degree_model,
    pagination_parser,
    custom_schema_pagination,
    paginated_degree_model,
)


degree_ns = Namespace(name="degree", description="degree of teachers")


@degree_ns.route("")
class DegreeList(Resource):
    """Shows a list of all degrees, and lets you POST to add new degree"""

    @degree_ns.expect(pagination_parser)
    @degree_ns.marshal_with(paginated_degree_model)
    def get(self):
        """List all degrees"""
        return pagination.paginate(
            Degree, degree_model, pagination_schema_hook=custom_schema_pagination
        )

    @degree_ns.expect(degree_model, pagination_parser)
    @degree_ns.marshal_with(paginated_degree_model)
    def post(self):
        """Adds a new degree"""
        degree = Degree()
        for key, value in degree_ns.payload.items():
            setattr(degree, key, value)
        db.session.add(degree)
        db.session.commit()
        return pagination.paginate(
            Degree, degree_model, pagination_schema_hook=custom_schema_pagination
        )


def get_degree_or_404(id):
    degree = Degree.query.get(id)
    if not degree:
        abort(404, "Degree not found")
    return degree


@degree_ns.route("/<int:id>")
@degree_ns.response(404, "Degree not found")
@degree_ns.param("id", "The degree's unique identifier")
class DegreesDetail(Resource):
    """Show a degree and lets you delete and modify it"""

    @degree_ns.marshal_with(degree_model)
    def get(self, id):
        """Fetch the degree with a given id"""
        return get_degree_or_404(id)

    @degree_ns.expect(degree_model, pagination_parser, validate=False)
    @degree_ns.marshal_with(paginated_degree_model)
    def patch(self, id):
        """Update the degree with a given id"""
        degree = get_degree_or_404(id)
        degree_keys = degree_model.keys()
        for key, value in degree_ns.payload.items():
            if key in degree_keys:
                setattr(degree, key, value)
        db.session.commit()
        return pagination.paginate(
            Degree, degree_model, pagination_schema_hook=custom_schema_pagination
        )

    @degree_ns.expect(pagination_parser)
    @degree_ns.marshal_with(paginated_degree_model)
    def delete(self, id):
        """Delete the degree with a given id"""
        degree = get_degree_or_404(id)
        db.session.delete(degree)
        db.session.commit()
        return pagination.paginate(
            Degree, degree_model, pagination_schema_hook=custom_schema_pagination
        )
