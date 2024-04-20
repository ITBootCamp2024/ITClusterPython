from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, Assessment
from project.schemas.assessment import assessment_model
from project.schemas.authorization import authorizations
from project.validators import allowed_roles


assessment_ns = Namespace(
    name="assessment", description="Assessment info", authorizations=authorizations
)


@assessment_ns.route("/create")
class AssessmentCreate(Resource):
    """Create a new assessment"""

    @allowed_roles(["teacher", "admin", "content_manager"])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.expect(assessment_model)
    def post(self):
        """Create a new assessment"""
        syllabus_id = assessment_ns.payload.get("syllabus_id")
        syllabus = Syllabus.query.filter_by(id=syllabus_id).first()

        if not syllabus:
            abort(400, f"Syllabus with id {syllabus_id} not found")

        assessment = Assessment(
            syllabus_id=syllabus_id,
            object=assessment_ns.payload.get("object"),
            method=assessment_ns.payload.get("method"),
            tool=assessment_ns.payload.get("tool"),
        )
        db.session.add(assessment)
        db.session.commit()

        return assessment

