from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, Assessment
from project.schemas.assessment import assessment_model
from project.schemas.authorization import authorizations
from project.validators import allowed_roles


assessment_ns = Namespace(
    name="assessment", description="Assessment info", authorizations=authorizations
)


def get_assessment_or_404(id):
    assessment = Assessment.query.get(id)
    if not assessment:
        abort(404, "Assessment not found")
    return assessment


def get_assessment_response():
    assessment = Assessment.query.all()
    return {
        "content": assessment,
        "totalElements": len(assessment)
    }


@assessment_ns.route("/create/<int:syllabus_id>")
class AssessmentCreate(Resource):
    """Create a new assessment"""

    @allowed_roles(["teacher", "admin", "content_manager"])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.expect(assessment_model)
    def post(self, syllabus_id):
        """Create a new assessment"""

        # syllabus_id = assessment_ns.payload.get("syllabus_id")
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


@assessment_ns.route("/<int:id>")
@assessment_ns.response(404, "Assessment not found")
@assessment_ns.param("id", "The assessment unique identifier")
class TeachersDetail(Resource):
    """Show a assessment and lets you delete him"""

    @assessment_ns.marshal_with(assessment_model)
    def get(self, id):
        """Fetch the assessment with a given id"""
        return get_assessment_or_404(id)

    @assessment_ns.expect(assessment_model, validate=False)
    @assessment_ns.marshal_with(assessment_model)
    def patch(self, id):
        """Update the assessment with a given id"""
        assessment = get_assessment_or_404(id)
        plain_params = ["syllabus_id", "object", "method", "tool"]
        for key, value in assessment_ns.payload.items():
            if key in plain_params:
                setattr(assessment, key, value)

        db.session.commit()
        return Assessment.query.all()

    @allowed_roles(["teacher", "admin", "content_manager"])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.marshal_with(assessment_model)
    def delete(self, id):
        """Delete the assessment with given id"""
        assessment = get_assessment_or_404(id)
        db.session.delete(assessment)
        db.session.commit()
        return Assessment.query.all()
