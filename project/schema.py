import re

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


position_model = api.model(
    "Position",
    {
        "id": fields.Integer(
            readonly=True, description="Position unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="Position name",
            min_length=1,
            max_length=100,
        )
    }
)


degree_model = api.model(
    "Degree",
    {
        "id": fields.Integer(
            readonly=True, description="Degree unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="Degree name",
            min_length=1,
            max_length=45,
        )
    }
)


teacher_model = api.model(  # TODO: change model
    "Teacher",
    {
        "id": fields.Integer(
            readonly=True, description="The teacher unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the teacher",
            min_length=1,
            max_length=100,
        ),
        "position": fields.String(
            required=True,
            description="The position of the teacher",
            min_length=1,
            max_length=100,
        ),
        "degree": fields.String(
            required=True,
            description="The teacher's degree",
            min_length=0,
            max_length=100,
        ),
        "university": fields.String(
            required=True,
            description="Teacher's university",
            min_length=0,
            max_length=100,
        ),
        "department": fields.String(
            required=True,
            description="Teacher's department",
            min_length=0,
            max_length=100,
        ),
        "email": fields.String(
            required=True,
            description="The teacher's email",
            min_length=0,
            max_length=100,
        ),
        "comments": fields.String(
            required=True,
            description="Some comments to the teacher",
            min_length=0,
            max_length=100,
        ),
    },
)


university_model = api.model(
    "University",
    {
        "id": fields.Integer(
            readonly=True, description="The program level unique identifier",
        ),
        "name": fields.String(description="The program level name",
                              min_length=5, max_length=100,),
        "shortname": fields.String(description="University abbreviation",
                                   min_length=2, max_length=20,),
        "sitelink": fields.String(description="University site"),
        "programs_list": fields.String(description="Url for the list of programs")
    },
)


school_model = api.model(
    "school",
    {
        "id": fields.Integer(
            readonly=True, description="School ID"
        ),
        "name": fields.String(description="School name"),
        "site": fields.String(required=False,  description="School site",
                              min_length=10, max_length=100,),
        "description": fields.String(required=False, description="Brief description",
                                     min_length=20, max_length=400,),
        "contact": fields.String(required=False, description="School contacts",
                                 min_length=5, max_length=100,),
        "university_id": fields.Integer(description="Related University ID",
                                        min_length=1)
    },
)


program_model = api.model(
    "Program",
    {
        "id": fields.Integer(
            readonly=True, description="The program's unique identifier"
        ),
        "name": fields.String(
            required=True,
            description="The name of the program",
            min_length=1,
            max_length=200,
        ),
        "specialty_id": fields.Integer(
            required=True,
            description="id of the specialty",
            min=1
        ),
        "program_link": fields.String(
            required=True,
            description="The link to the program",
            min_length=0,
            max_length=200,
        ),
        "university_id": fields.Integer(
            required=True,
            description="id of the university",
            min=1
        ),
        "level": fields.Integer(
            required=True,
            description="id of the level",
            min=1
        ),
        "garant": fields.String(
            required=True,
            description="Garant's name",
            min_length=0,
            max_length=100,
        ),
        "school_name": fields.String(
            required=True,
            description="The name of the school",
            min_length=0,
            max_length=200,
        ),
        "school_link": fields.String(
            required=True,
            description="The school's link",
            min_length=0,
            max_length=200,
        ),
        "clabus_link": fields.String(
            required=True,
            description="The clabus's link",
            min_length=0,
            max_length=200,
        )
    }
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


program_parser = api.parser()
program_parser.add_argument(
    "specialty_id", type=int, required=False, default=0, help="Specialty ID"
)
program_parser.add_argument(
    "university_id", type=int, required=False, default=0, help="University ID"
)
program_parser.add_argument(
    "level", type=int, required=False, default=0, help="Level ID"
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


paginated_specialty_model = get_pagination_schema_for(specialty_model)
paginated_teacher_model = get_pagination_schema_for(teacher_model)
paginated_university_model = get_pagination_schema_for(university_model)
paginated_school_model = get_pagination_schema_for(school_model)
paginated_program_model = get_pagination_schema_for(program_model)
paginated_position_model = get_pagination_schema_for(position_model)
paginated_degree_model = get_pagination_schema_for(degree_model)

