import re

from flask_restx import fields

from project.extensions import api


pagination_parser = api.parser()
pagination_parser.add_argument(
    "page", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "size",
    type=int,
    required=False,
    default=20,
    help="Page size (number of items per page)",
)


def custom_schema_pagination(current_page, page_obj):
    schema_pagination = {
        # "next": page_obj.has_next,
        # "prev": page_obj.has_prev,
        "pageNumber": current_page,
        # "pages": page_obj.pages,
        # "per_page": page_obj.per_page,
        "totalElements": page_obj.total,
    }
    page = re.search(r"page=(\d+)", current_page)
    if page:
        schema_pagination["pageNumber"] = int(page.group(1))
    return schema_pagination


def get_pagination_schema_for(response_model: api.model):
    return api.model(
        f"Pagination({response_model.name})",
        {
            "content": fields.List(fields.Nested(response_model)),
            # "next": fields.String(
            #     requred=True,
            #     description="Link to the next page",
            #     default='link/to/the/next/page'
            # ),
            # "prev": fields.String(
            #     required=True,
            #     description="Link to the previous page",
            #     default='link/to/the/previous/page'
            # ),
            "pageNumber": fields.Integer(
                required=True,
                description="Current page number",
                default=1),
            # "pages": fields.Integer(required=True, description="Total number of pages"),
            # "per_page": fields.Integer(required=True, description="Number of items per page"),
            "totalElements": fields.Integer(required=True, description="Total number of items"),
        },
    )
