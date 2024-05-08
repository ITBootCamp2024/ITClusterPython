from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import MarketRelation, Roles
from project.routes.syllabus import get_syllabus_or_404, set_syllabus_filling_status
from project.schemas.authorization import authorizations
from project.schemas.market_relation import (
    market_relation_response_model,
    market_relation_model,
)
from project.validators import allowed_roles, verify_teacher

market_relation_ns = Namespace(
    "syllabuses/market-relation",
    description="Market relations",
    authorizations=authorizations,
)


def create_market_relations(syllabus_id, market_relations):

    for fields in market_relations:
        market_relation = MarketRelation(
            syllabus_id=syllabus_id,
            specialty=fields.get("specialty"),
            vacancies=fields.get("vacancies"),
            skills=fields.get("skills"),
            relevant_materials=fields.get("relevant_materials"),
            borrowed_materials=fields.get("borrowed_materials"),
        )
        db.session.add(market_relation)

    db.session.commit()


def get_market_relation_or_404(relation_id):
    market_relation = MarketRelation.query.get(relation_id)
    if not market_relation:
        abort(404, f"Market relation with id {relation_id} not found")
    return market_relation


def get_market_relation_response(syllabus_id):
    market_relations = (
        db.session.query(MarketRelation).filter_by(syllabus_id=syllabus_id).all()
    )
    return {
        "market_relations": market_relations,
        "syllabus_id": syllabus_id,
    }


@market_relation_ns.route("/<int:syllabus_id>")
@market_relation_ns.param("syllabus_id", "The syllabus unique identifier")
class MarketRelationsList(Resource):
    """Get market relation or create a new market relation"""

    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    def get(self, syllabus_id):
        """Get market relation by given syllabus_id"""
        return get_market_relation_response(syllabus_id)

    @market_relation_ns.expect(market_relation_response_model)
    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def post(self, syllabus_id):
        """Create a new market relation"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        create_market_relations(
            syllabus_id, market_relation_ns.payload.get("market_relations")
        )

        set_syllabus_filling_status(syllabus_id)

        return get_market_relation_response(syllabus_id)


@market_relation_ns.route("/<int:relation_id>")
@market_relation_ns.param("relation_id", "The market relation unique identifier")
class MarketRelationsDetail(Resource):

    @market_relation_ns.expect(market_relation_model, validate=False)
    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def patch(self, relation_id):
        """Modify market relation of given relation_id"""

        market_relation = get_market_relation_or_404(relation_id)
        syllabus = market_relation.syllabus
        verify_teacher(syllabus)

        params = market_relation_model.keys()
        for key, value in market_relation_ns.payload.items():
            if key in params:
                setattr(market_relation, key, value)
        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_market_relation_response(syllabus.id)

    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles([Roles.TEACHER, Roles.ADMIN, Roles.CONTENT_MANAGER])
    def delete(self, relation_id):
        """Delete the market relation with given relation_id"""

        market_relation = get_market_relation_or_404(relation_id)
        syllabus = market_relation.syllabus
        verify_teacher(syllabus)

        db.session.delete(market_relation)
        db.session.commit()

        set_syllabus_filling_status(syllabus.id)

        return get_market_relation_response(syllabus.id)
