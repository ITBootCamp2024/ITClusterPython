from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model
from project.schemas.graduate_task import graduate_task_response_model
from project.schemas.self_study import self_study_topic_response_model

base_structure_topics_model = api.model(
    "StructureTopics",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the structure topic",
            default=1,
        ),
        "theoretical_topic": fields.String(
            required=True,
            description="Theoretical topic",
            max_length=255,
        ),
        "theoretical_hours": fields.Integer(
            description="Theoretical hours",
        ),
        "practice_topics": fields.String(
            description="Practice topics",
            max_length=255,
        ),
        "practice_hours": fields.Integer(
            description="Practice hours",
        ),
        "technologies": fields.String(description="Technologies"),
    },
)

base_syllabus_module_model = api.model(
    "BaseSyllabusModule",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the syllabus module",
            default=1,
        ),
        "name": fields.String(
            required=True,
            description="Syllabus module name",
            max_length=255,
            default="syllabus module name",
        ),
    },
)
syllabus_module_model = api.model(
    "SyllabusModule",
    {
        **base_syllabus_module_model,
        "topics": fields.List(fields.Nested(base_structure_topics_model)),
    },
)

syllabus_module_response_model = api.model(
    "SyllabusModuleResponse",
    {
        "modules": fields.List(fields.Nested(syllabus_module_model), required=True),
        **syllabus_id_model,
    },
)

syllabus_structure_three_model = api.model(
    "SyllabusStructureThree",
    {
        **syllabus_module_response_model,
        **self_study_topic_response_model,
        **graduate_task_response_model,
    }
)
