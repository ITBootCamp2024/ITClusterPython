from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import SyllabusModule, DisciplineStructure, Roles
from project.routes.graduate_task import get_graduate_task_response
from project.routes.self_study import get_self_study_response
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.authorization import authorizations
from project.schemas.discipline_structure import (
    syllabus_module_response_model,
    base_syllabus_module_model,
    base_structure_topics_model,
    syllabus_structure_three_model,
)
from project.validators import allowed_roles, verify_teacher

discipline_structure_ns = Namespace(
    "syllabuses/structure",
    description="Syllabus discipline structure",
    authorizations=authorizations,
)


def add_syllabus_modules(syllabus_id):
    modules = discipline_structure_ns.payload.get("modules")
    if not modules:
        abort(400, "Modules are required")

    for module in modules:
        syllabus_module = SyllabusModule(
            syllabus_id=syllabus_id,
            name=module.get("name"),
        )
        db.session.add(syllabus_module)
        db.session.commit()

        module_id = syllabus_module.id
        topics = module.get("topics")
        for topic in topics:
            syllabus_topic = DisciplineStructure(
                module_id=module_id,
                theoretical_topic=topic.get("theoretical_topic"),
                theoretical_hours=topic.get("theoretical_hours"),
                practice_topics=topic.get("practice_topics"),
                practice_hours=topic.get("practice_hours"),
                technologies=topic.get("technologies"),
            )
            db.session.add(syllabus_topic)
        db.session.commit()


def delete_modules(syllabus_id):
    modules = SyllabusModule.query.filter_by(syllabus_id=syllabus_id).all()
    for module in modules:
        db.session.delete(module)
    db.session.commit()


def delete_module(module_id):
    module = SyllabusModule.query.get(module_id)
    db.session.delete(module)
    db.session.commit()


def get_syllabus_module_or_404(module_id):
    module = SyllabusModule.query.get(module_id)
    if not module:
        abort(404, f"Module with id {module_id} not found")
    return module


def get_syllabus_modules_response(syllabus_id):
    """Get list of syllabus modules"""
    modules = SyllabusModule.query.filter_by(syllabus_id=syllabus_id).all()
    return {
        "modules": modules,
        "syllabus_id": syllabus_id,
    }


def get_syllabus_structure_three_response(syllabus_id):
    return {
        **get_syllabus_modules_response(syllabus_id),
        **get_self_study_response(syllabus_id),
        **get_graduate_task_response(syllabus_id),
    }


def get_syllabus_topic_or_404(topic_id):
    topic = DisciplineStructure.query.get(topic_id)
    if not topic:
        abort(404, f"Topic with id {topic_id} not found")
    return topic


@discipline_structure_ns.route("/3/<int:syllabus_id>")
@discipline_structure_ns.param("syllabus_id", "The syllabus unique identifier")
class SyllabusStructureList(Resource):
    """Show 3 tables of discipline structure"""

    @discipline_structure_ns.marshal_with(
        syllabus_structure_three_model, envelope="content"
    )
    def get(self, syllabus_id):
        """Get 3 tables of discipline structure by given syllabus_id"""
        return get_syllabus_structure_three_response(syllabus_id)


@discipline_structure_ns.route("/<int:syllabus_id>")
@discipline_structure_ns.param("syllabus_id", "The syllabus unique identifier")
class DisciplineStructureList(Resource):
    """Show a list of syllabus modules"""

    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    def get(self, syllabus_id):
        """Get list of syllabus modules by given syllabus_id"""
        return get_syllabus_modules_response(syllabus_id)

    @discipline_structure_ns.expect(syllabus_module_response_model)
    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, syllabus_id):
        """Create new syllabus modules"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)
        add_syllabus_modules(syllabus_id)

        set_syllabus_filling_status(syllabus_id)

        return get_syllabus_modules_response(syllabus_id)


@discipline_structure_ns.route("/module/<int:module_id>")
@discipline_structure_ns.param("module_id", "The syllabus module unique identifier")
class DisciplineStructureModuleDetail(Resource):

    @discipline_structure_ns.expect(base_structure_topics_model)
    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, module_id):
        """Add syllabus topic to module with given module_id"""
        module = get_syllabus_module_or_404(module_id)
        syllabus = module.syllabus
        verify_teacher(syllabus)

        syllabus_topic = DisciplineStructure(module_id=module_id)
        params = base_structure_topics_model.keys()
        for key, value in discipline_structure_ns.payload.items():
            if key in params:
                setattr(syllabus_topic, key, value)
        db.session.add(syllabus_topic)
        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_syllabus_modules_response(syllabus.id)

    @discipline_structure_ns.expect(base_syllabus_module_model)
    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, module_id):
        """Modify syllabus module"""
        module = get_syllabus_module_or_404(module_id)
        syllabus = module.syllabus
        verify_teacher(syllabus)
        module.name = discipline_structure_ns.payload.get("name")
        db.session.commit()
        set_syllabus_filling_status(syllabus.id)

        return get_syllabus_modules_response(syllabus.id)

    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, module_id):
        """Delete syllabus module"""
        module = get_syllabus_module_or_404(module_id)
        syllabus = module.syllabus
        verify_teacher(syllabus)
        delete_module(module_id)
        set_syllabus_filling_status(syllabus.id)

        return get_syllabus_modules_response(syllabus.id)


@discipline_structure_ns.route("/topic/<int:topic_id>")
@discipline_structure_ns.param("topic_id", "The syllabus topic unique identifier")
class DisciplineStructureTopicDetail(Resource):

    @discipline_structure_ns.expect(base_structure_topics_model)
    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, topic_id):
        """Modify syllabus topic"""
        topic = get_syllabus_topic_or_404(topic_id)
        syllabus = topic.module.syllabus
        verify_teacher(syllabus)
        topic_params = base_structure_topics_model.keys()
        for key, value in discipline_structure_ns.payload.items():
            if key in topic_params:
                setattr(topic, key, value)
        db.session.commit()
        set_syllabus_filling_status(syllabus.id)

        return get_syllabus_modules_response(syllabus.id)

    @discipline_structure_ns.marshal_with(
        syllabus_module_response_model, envelope="content"
    )
    @discipline_structure_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, topic_id):
        """Delete syllabus topic"""
        topic = get_syllabus_topic_or_404(topic_id)
        syllabus = topic.module.syllabus
        verify_teacher(syllabus)
        db.session.delete(topic)
        db.session.commit()
        set_syllabus_filling_status(syllabus.id)

        return get_syllabus_modules_response(syllabus.id)
