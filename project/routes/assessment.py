from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Syllabus, Assessment
from project.schemas.assessment import assessment_model, assessment_response_model
from project.schemas.authorization import authorizations
from project.validators import allowed_roles

assessment_ns = Namespace(
    name="syllabuses/assessments", description="Assessment info", authorizations=authorizations
)


def get_assessment_or_404(id):
    assessment = Assessment.query.get(id)
    if not assessment:
        abort(404, "Assessment not found")
    return assessment


def get_assessment_response(syllabus_id):
    assessments = db.session.query(Assessment).filter_by(syllabus_id=syllabus_id).all()
    return {
        "assessments": assessments,
    }


@assessment_ns.route("/<int:syllabus_id>")
@assessment_ns.param("syllabus_id", "The syllabus unique identifier")
class AssessmentsList(Resource):
    """Get list of assessments or create a new assessment"""

    @assessment_ns.marshal_with(assessment_response_model)
    def get(self, syllabus_id):
        """Get list of assessments by given syllabus_id"""
        return get_assessment_response(syllabus_id)

    @assessment_ns.marshal_with(assessment_response_model)
    @allowed_roles(["teacher", "admin", "content_manager"])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.expect(assessment_model)
    def post(self, syllabus_id):
        """Create a new assessment"""

        syllabus = Syllabus.query.filter_by(id=syllabus_id).first()

        if not syllabus:
            abort(400, f"Syllabus with id {syllabus_id} not found")

        if (get_jwt().get("role") == "teacher" and
                syllabus.teacher.email != get_jwt_identity()):
            abort(403, "You are not the teacher of this syllabus")

        assessment = Assessment(
            syllabus_id=syllabus_id,
            object=assessment_ns.payload.get("object"),
            method=assessment_ns.payload.get("method"),
            tool=assessment_ns.payload.get("tool"),
        )
        db.session.add(assessment)
        db.session.commit()

        return get_assessment_response(syllabus_id)


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
    @assessment_ns.marshal_with(assessment_response_model)
    @assessment_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def patch(self, id):
        """Update the assessment with a given id"""
        assessment = get_assessment_or_404(id)
        syllabus = assessment.syllabus

        if (get_jwt().get("role") == "teacher" and
                syllabus.teacher.email != get_jwt_identity()):
            abort(403, "You are not the teacher of this syllabus")

        plain_params = ["object", "method", "tool"]
        for key, value in assessment_ns.payload.items():
            if key in plain_params:
                setattr(assessment, key, value)

        db.session.commit()
        return get_assessment_response(syllabus.id)

    @allowed_roles(["teacher", "admin", "content_manager"])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.marshal_with(assessment_response_model)
    def delete(self, id):
        """Delete the assessment with given id"""
        assessment = get_assessment_or_404(id)
        syllabus = assessment.syllabus
        if (get_jwt().get("role") == "teacher" and
                syllabus.teacher.email != get_jwt_identity()):
            abort(403, "You are not the teacher of this syllabus")

        db.session.delete(assessment)
        db.session.commit()
        return get_assessment_response(syllabus.id)