from project.extensions import api
from flask_restx import fields

program_level_model = api.model(
    "ProgramLevel",
    {
        "id": fields.Integer(
            readonly=True, description="The program level unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The program level name",
            min_length=1,
            max_length=100,
        ),
    },
)

course_blocks_model = api.model(
    "CourseBlocks",
    {
        "id": fields.Integer(readonly=True, description="The course unique identifier"),
        "name": fields.String(
            required=True, description="The course name", min_length=1, max_length=100
        ),
        "description": fields.String(
            required=True, description="The course description"
        ),
    },
)

course_statuses_model = api.model(
    "CourseStatuses",
    {
        "id": fields.Integer(readonly=True, description="The status unique identifier"),
        "name": fields.String(
            required=True, description="The status name", min_length=1, max_length=100
        ),
        "description": fields.String(description="The status description"),
    },
)

course_groupes_model = api.model(
    "CourseGroupes",
    {
        "id": fields.Integer(
            readonly=True, description="The course_group unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The course_group name",
            min_length=1,
            max_length=100,
        ),
        "description": fields.String(description="The course_group description"),
        "type_id": fields.Integer(min=1),
    },
)

specialty_model = api.model(
    "Specialty",
    {
        "id": fields.Integer(
            required=True, description="The specialty unique identifier", min=0, max=500
        ),
        "name": fields.String(
            required=True,
            description="The name of the specialty",
            min_length=1,
            max_length=200,
        ),
        "link_standart": fields.String(
            required=True,
            description="The link to the specialty",
            min_length=0,
            max_length=200,
        ),
    },
)

teacher_model = api.model(
    "Teacher",
    {
        "id": fields.Integer(
            readonly=True, description="The teacher unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the teacher",
            min_length=1,
            max_length=50,
        ),
        "role": fields.String(
            required=True,
            description="The role of the teacher",
            min_length=1,
            max_length=50,
        ),
        "status": fields.String(
            required=True,
            description="The status of the teacher",
            min_length=0,
            max_length=100,
        ),
        "email": fields.String(
            required=True,
            description="The email of the teacher",
            min_length=0,
            max_length=100,
        ),
        "details": fields.String(
            required=True,
            description="The details of the teacher",
            min_length=0,
            max_length=100,
        ),
    },
)

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
    return {
        "next": page_obj.has_next,
        "prev": page_obj.has_prev,
        "current": current_page,
        "pages": page_obj.pages,
        "per_page": page_obj.per_page,
        "total": page_obj.total,
    }


def get_pagination_schema_for(response_model: api.model):
    return api.model(
        "Pagination",
        {
            "data": fields.List(fields.Nested(response_model)),
            "next": fields.String(
                requred=True,
                description="Link to the next page",
                default='link/to/the/next/page'
            ),
            "prev": fields.String(
                required=True,
                description="Link to the previous page",
                default='link/to/the/previous/page'
            ),
            "current": fields.String(
                required=True,
                description="Current page link",
                default='link/to/the/current/page'),
            "pages": fields.Integer(required=True, description="Total number of pages"),
            "per_page": fields.Integer(required=True, description="Number of items per page"),
            "total": fields.Integer(required=True, description="Total number of items"),
        },
    )


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
