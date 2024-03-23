from flask_restx.fields import List

from project.extensions import api
from flask_restx import fields


university_model = api.model(
    "University",
    {
        "id": fields.Integer(
            readonly=True, description="The program level unique identifier",
        ),
        "name": fields.String(required=True, description="The program level name",
                              min_length=5, max_length=100,),
        "shortname": fields.String(description="University abbreviation",
                                   min_length=2, max_length=20,),
        "sitelink": fields.String(description="University site", absolute=False),
        "programs_list": fields.String(description="Url for the list of programs")
    },
)


school_model = api.model(
    "school",
    {
        "id": fields.Integer(
            readonly=True, description="School ID"
        ),
        "name": fields.String(required=True, description="School name"),
        "size": fields.String(required=False,  description="School size",
                              min_length=2, max_length=100,),
        "description": fields.String(required=False, description="Brief description",
                                     min_length=20, max_length=400,),
        "contact": fields.String(required=False, description="School contacts",
                                 min_length=5, max_length=100,),
        "university_id": fields.Integer(required=True, description="Related University ID",
                                        min_length=1)
    },
)


pagination_parser = api.parser()
pagination_parser.add_argument(
    "page", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "size", type=int, required=False, default=20, help="Page size (number of items per page)"
)