from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import SelfStudyTopic, Roles
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.authorization import authorizations
from project.schemas.self_study import (
    self_study_topic_response_model,
    self_study_topic_model,
)
from project.validators import allowed_roles, verify_teacher

self_study_topics_ns = Namespace(
    "syllabuses/self-study",
    description="Self study topics",
    authorizations=authorizations,
)


def create_self_study_topics(syllabus_id, topics):

    for fields in topics:
        self_study_topic = SelfStudyTopic(
            syllabus_id=syllabus_id,
            name=fields.get("name"),
            controls=fields.get("controls"),
            hours=fields.get("hours"),
        )
        db.session.add(self_study_topic)

    db.session.commit()


def get_self_study_topic_or_404(id):
    topic = SelfStudyTopic.query.get(id)
    if not topic:
        abort(404, f"Self study topic with id {id} not found")
    return topic


def get_self_study_response(syllabus_id):
    topics = db.session.query(SelfStudyTopic).filter_by(syllabus_id=syllabus_id).all()
    return {
        "self_study_topics": topics,
        "syllabus_id": syllabus_id,
    }


@self_study_topics_ns.route("/<int:syllabus_id>")
@self_study_topics_ns.param("syllabus_id", "The syllabus unique identifier")
class SelfStudyTopicsList(Resource):
    """Get list of self study topics or create a new self study topic"""

    @self_study_topics_ns.marshal_with(
        self_study_topic_response_model, envelope="content"
    )
    def get(self, syllabus_id):
        """Get list of self study topics by given syllabus_id"""
        return get_self_study_response(syllabus_id)

    @self_study_topics_ns.expect(self_study_topic_response_model)
    @self_study_topics_ns.marshal_with(
        self_study_topic_response_model, envelope="content"
    )
    @self_study_topics_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, syllabus_id):
        """Create a new topic for self study"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        create_self_study_topics(
            syllabus_id, self_study_topics_ns.payload.get("self_study_topics")
        )

        set_syllabus_filling_status(syllabus_id)

        return get_self_study_response(syllabus_id)


@self_study_topics_ns.route("/<int:topic_id>")
@self_study_topics_ns.param("topic_id", "The topic unique identifier")
class SelfStudyTopicDetail(Resource):
    """Show a self study topic and lets you modify or delete it"""

    @self_study_topics_ns.expect(self_study_topic_model, validate=False)
    @self_study_topics_ns.marshal_with(
        self_study_topic_response_model, envelope="content"
    )
    @self_study_topics_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, topic_id):
        """Update the topic with a given id"""
        topic = get_self_study_topic_or_404(topic_id)
        syllabus = topic.syllabus
        verify_teacher(syllabus)

        plain_params = ["name", "controls", "hours"]
        for key, value in self_study_topics_ns.payload.items():
            if key in plain_params:
                setattr(topic, key, value)

        db.session.commit()
        set_syllabus_filling_status(syllabus.id)

        return get_self_study_response(syllabus.id)

    @self_study_topics_ns.marshal_with(
        self_study_topic_response_model, envelope="content"
    )
    @self_study_topics_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, topic_id):
        """Delete the topic with a given id"""

        topic = get_self_study_topic_or_404(topic_id)
        syllabus = topic.syllabus
        verify_teacher(syllabus)

        db.session.delete(topic)
        db.session.commit()
        set_syllabus_filling_status(syllabus.id)

        return get_self_study_response(syllabus.id)
