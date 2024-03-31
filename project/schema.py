import re

from project.extensions import api
from flask_restx import fields


base_id_model = api.model(
    "BaseID",
    {
        "id": fields.Integer(description="The unique identifier", required=True, default=1),
    }
)


base_name_model = api.model(
    "BaseName",
    {
        "name": fields.String(
            required=True,
            description="The name of the object",
        )
    }
)


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


short_discipline_blocks_model = api.model(
    "ShortDisciplineBlocks",
    {
        "id": fields.Integer(readonly=True, description="The unique identifier of discipline block"),
        "name": fields.String(
            required=True, description="The discipline block name", min_length=1, max_length=255
        ),
    }
)


discipline_blocks_model = api.model(
    "DisciplineBlock",
    {
        **short_discipline_blocks_model,
        "description": fields.String(
            description="The discipline block description"
        ),
    },
)


base_discipline_groups_model = api.model(
    "BaseDisciplineGroups",
    {
        "id": fields.Integer(
            readonly=True, description="The unique identifier of discipline group"
        ),
        "name": fields.String(
            required=True,
            description="The discipline group name",
            min_length=1,
            max_length=100,
        ),
        "description": fields.String(description="The discipline group description"),
        "discipline_url": fields.String(
            description="The link to the discipline group",
            max_length=255
        )
    }
)


discipline_groups_model = api.model(
    "DisciplineGroup",
    {
        **base_discipline_groups_model,
        "block": fields.Nested(short_discipline_blocks_model)
    },
)


discipline_groups_query_model = api.model(
    "DisciplineGroupsQuery",
    {
        **base_discipline_groups_model,
        "block": fields.Nested(base_id_model, required=True)
    }
)


specialty_model = api.model(
    "Specialty",
    {
        "id": fields.Integer(
            readonly=True, description="The specialty unique identifier"
        ),
        "code": fields.String(
            required=True,
            description="The code of the specialty",
            max_length=45,
        ),
        "name": fields.String(
            required=True,
            description="The name of the specialty",
            min_length=1,
            max_length=100,
        ),
        "standard_url": fields.String(
            description="The link to the specialty",
            max_length=255,
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


short_university_model = api.model(
    "ShortUniversity",
    {
        "id": fields.Integer(
            readonly=True,
            description="The unique identifier of the university",
        ),
        "name": fields.String(
            required=True,
            description="Name of the university",
            min_length=5,
            max_length=150,),
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
            min_length=3,
            max_length=100,),
    }
)


base_teacher_model = api.model(
    "BaseTeacher",
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
        "email": fields.String(
            required=True,
            description="The teacher's email",
            min_length=0,
            max_length=100,
        ),
        "comments": fields.String(
            required=True,
            description="Some comments to the teacher",
            min_length=0
        )
    }
)

teacher_model = api.model(
    "Teacher",
    {
        **base_teacher_model,
        "position": fields.Nested(position_model),
        "degree": fields.Nested(degree_model),
        "university": fields.Nested(short_university_model),
        "department": fields.Nested(short_department_model),
    }
)


teacher_query_model = api.inherit(
    "TeacherQuery",
    {
        **base_teacher_model,
        "position": fields.Nested(base_id_model, required=True),
        "degree": fields.Nested(base_id_model, required=True),
        "department": fields.Nested(base_id_model, required=True)
    }
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
paginated_school_model = get_pagination_schema_for(school_model)  # TODO delete this model
paginated_program_model = get_pagination_schema_for(program_model)
paginated_position_model = get_pagination_schema_for(position_model)
paginated_degree_model = get_pagination_schema_for(degree_model)
paginated_discipline_blocks_model = get_pagination_schema_for(discipline_blocks_model)
paginated_discipline_groups_model = get_pagination_schema_for(discipline_groups_model)
