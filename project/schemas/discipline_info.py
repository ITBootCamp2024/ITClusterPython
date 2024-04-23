from flask_restx import fields

from project.extensions import api
from project.schemas.general import syllabus_id_model

discipline_info_model = api.model(
    "DisciplineInfo",
    {
        "id": fields.Integer(
            readonly=True,
            description="Unique identifier of the discipline_info",
            default=1,
        ),
        "program_url": fields.String(description="Program URL"),
        "abstract": fields.String(description="Short abstract"),
        "goal": fields.String(description="Goal"),
        "competencies_list": fields.String(description="Competencies list"),
        "technologies_list": fields.String(description="Technologies list"),
        "graduate_task": fields.String(description="Graduate task"),
        "lecture": fields.Integer(description="Lecture hours"),
        "laboratory": fields.Integer(description="Laboratory hours"),
        "practice": fields.Integer(description="Practice hours"),
        "self_study": fields.Integer(description="Self-study hours"),
        "required_skills": fields.String(description="Required skills"),
        "university_logistics": fields.String(description="University logistics"),
        "self_logistics": fields.String(description="Self logistics"),
    },
)

discipline_info_response_model = api.model(
    "DisciplineInfoResponse",
    {
        "discipline_info": fields.Nested(
            discipline_info_model, required=True, allow_null=True
        ),
        **syllabus_id_model,
    },
)
