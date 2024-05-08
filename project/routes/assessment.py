from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import Assessment, Roles
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.assessment import assessment_model, assessment_response_model
from project.schemas.authorization import authorizations
from project.validators import allowed_roles, verify_teacher

assessment_ns = Namespace(
    name="syllabuses/assessments",
    description="Assessment info",
    authorizations=authorizations,
)


def create_assessments(syllabus_id, assessments):

    for fields in assessments:
        assessment = Assessment(
            syllabus_id=syllabus_id,
            object=fields.get("object"),
            method=fields.get("method"),
            tool=fields.get("tool"),
        )
        db.session.add(assessment)

    db.session.commit()


def get_assessment_or_404(id):
    assessment = Assessment.query.get(id)
    if not assessment:
        abort(404, "Assessment not found")
    return assessment


def get_assessment_response(syllabus_id):
    assessments = db.session.query(Assessment).filter_by(syllabus_id=syllabus_id).all()
    return {
        "assessments": assessments,
        "syllabus_id": syllabus_id,
    }


@assessment_ns.route("/<int:syllabus_id>")
@assessment_ns.param("syllabus_id", "The syllabus unique identifier")
class AssessmentsList(Resource):
    """Get list of assessments or create a new assessment"""

    @assessment_ns.marshal_with(assessment_response_model, envelope="content")
    def get(self, syllabus_id):
        """Get list of assessments by given syllabus_id"""
        return get_assessment_response(syllabus_id)

    @assessment_ns.marshal_with(assessment_response_model, envelope="content")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.expect(assessment_response_model)
    def post(self, syllabus_id):
        """Create a new assessment"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        create_assessments(syllabus_id, assessment_ns.payload.get("assessments"))

        set_syllabus_filling_status(syllabus_id)

        return get_assessment_response(syllabus_id)


@assessment_ns.route("/<int:assessment_id>")
@assessment_ns.param("assessment_id", "The assessment unique identifier")
class TeachersDetail(Resource):
    """Show an assessment and lets you modify or delete it"""

    @assessment_ns.expect(assessment_model, validate=False)
    @assessment_ns.marshal_with(assessment_response_model, envelope="content")
    @assessment_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, assessment_id):
        """Update the assessment with a given id"""
        assessment = get_assessment_or_404(assessment_id)
        syllabus = assessment.syllabus
        verify_teacher(syllabus)

        plain_params = ["object", "method", "tool"]
        for key, value in assessment_ns.payload.items():
            if key in plain_params:
                setattr(assessment, key, value)

        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_assessment_response(syllabus.id)

    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    @assessment_ns.doc(security="jsonWebToken")
    @assessment_ns.marshal_with(assessment_response_model, envelope="content")
    def delete(self, assessment_id):
        """Delete the assessment with given id"""
        assessment = get_assessment_or_404(assessment_id)
        syllabus = assessment.syllabus
        verify_teacher(syllabus)

        db.session.delete(assessment)
        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_assessment_response(syllabus.id)
