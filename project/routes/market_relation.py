from flask_restx import Resource, Namespace, abort

from project.extensions import db
from project.models import MarketRelation
from project.routes.syllabus import get_syllabus_or_404, verify_teacher
from project.schemas.authorization import authorizations
from project.schemas.market_relation import (
    market_relation_response_model,
    market_relation_model,
)
from project.validators import allowed_roles

market_relation_ns = Namespace(
    "syllabuses/market-relation",
    description="Market relations",
    authorizations=authorizations,
)


def get_market_relation_or_404(syllabus_id):
    market_relation = (
        db.session.query(MarketRelation).filter_by(syllabus_id=syllabus_id).first()
    )
    if not market_relation:
        abort(404, f"Market relation with syllabus_id {syllabus_id} not found")
    return market_relation


def get_market_relation_response(syllabus_id):
    market_relation = (
        db.session.query(MarketRelation).filter_by(syllabus_id=syllabus_id).first()
    )
    return {
        "market_relation": market_relation,
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

    @market_relation_ns.expect(market_relation_model)
    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def post(self, syllabus_id):
        """Create a new market relation"""

        syllabus = get_syllabus_or_404(syllabus_id)
        verify_teacher(syllabus)

        market_relation = MarketRelation(
            syllabus_id=syllabus_id,
            specialty=market_relation_ns.payload.get("specialty"),
            vacancies=market_relation_ns.payload.get("vacancies"),
            skills=market_relation_ns.payload.get("skills"),
            relevant_materials=market_relation_ns.payload.get("relevant_materials"),
            borrowed_materials=market_relation_ns.payload.get("borrowed_materials"),
        )
        db.session.add(market_relation)
        db.session.commit()

        return get_market_relation_response(syllabus_id)

    @market_relation_ns.expect(market_relation_model, validate=False)
    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def patch(self, syllabus_id):
        """Modify market relation of given syllabus_id"""

        market_relation = get_market_relation_or_404(syllabus_id)
        syllabus = market_relation.syllabus
        verify_teacher(syllabus)

        params = market_relation_model.keys()
        for key, value in market_relation_ns.payload.items():
            if key in params:
                setattr(market_relation, key, value)
        db.session.commit()

        return get_market_relation_response(syllabus_id)

    @market_relation_ns.marshal_with(market_relation_response_model, envelope="content")
    @market_relation_ns.doc(security="jsonWebToken")
    @allowed_roles(["teacher", "admin", "content_manager"])
    def delete(self, syllabus_id):
        """Delete the market relation with given id"""

        market_relation = get_market_relation_or_404(syllabus_id)
        syllabus = market_relation.syllabus
        verify_teacher(syllabus)

        db.session.delete(market_relation)
        db.session.commit()

        return get_market_relation_response(syllabus_id)
