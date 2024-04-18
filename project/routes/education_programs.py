from flask_restx import Resource, Namespace, abort
from sqlalchemy import desc

from project.extensions import db
from project.models import EducationProgram, Specialty, EducationLevel, University
from project.schemas.education_programs import (
    education_program_model,
    education_program_query_model
)
from project.schemas.service_info import serviced_education_program_model
from project.validators import validate_site


education_programs_ns = Namespace(name="education-programs", description="info about education programs")


def get_education_program_or_404(id):
    education_program = EducationProgram.query.get(id)
    if not education_program:
        abort(404, "Education program not found")
    return education_program


def get_education_program_response():
    education_programs = EducationProgram.query.order_by(desc("id")).all()
    specialties = Specialty.query.all()
    universities = University.query.all()
    education_levels = EducationLevel.query.all()
    return {
        "content": education_programs,
        "service_info": {
            "specialty": specialties,
            "university": universities,
            "education_levels": education_levels
        },
        "totalElements": len(education_programs)
    }


@education_programs_ns.route("")
class EducationProgramsList(Resource):
    """Shows a list of all education programs, and lets you POST to add new education program"""

    @education_programs_ns.marshal_with(serviced_education_program_model)
    def get(self):
        """List all education programs"""
        return get_education_program_response()

    @education_programs_ns.expect(education_program_query_model)
    @education_programs_ns.marshal_with(serviced_education_program_model)
    @validate_site('http', ["syllabus_url", "program_url"])
    def post(self):
        """Adds a new education program"""
        education_program = EducationProgram()
        plain_params = ["name", "program_url", "guarantor", "syllabus_url"]
        nested_ids = ["specialty", "education_level", "department"]
        for key, value in education_programs_ns.payload.items():
            if key in plain_params:
                setattr(education_program, key, value)
            elif key in nested_ids:
                setattr(education_program, key + "_id", value.get("id"))
        db.session.add(education_program)
        db.session.commit()
        return get_education_program_response()


@education_programs_ns.route("/<int:id>")
@education_programs_ns.response(404, "Education program not found")
@education_programs_ns.param("id", "The education program's unique identifier")
class EducationProgramsDetail(Resource):
    """Show a education program and lets you delete him"""

    @education_programs_ns.marshal_with(education_program_model)
    def get(self, id):
        """Fetch the education program with a given id"""
        return get_education_program_or_404(id)

    @education_programs_ns.expect(education_program_query_model, validate=False)
    @education_programs_ns.marshal_with(serviced_education_program_model)
    @validate_site('http', ["syllabus_url", "program_url"])
    def patch(self, id):
        """Update the education program with a given id"""
        education_program = get_education_program_or_404(id)
        plain_params = ["name", "program_url", "guarantor", "syllabus_url"]
        nested_ids = ["specialty", "education_level", "department"]
        for key, value in education_programs_ns.payload.items():
            if key in plain_params:
                setattr(education_program, key, value)
            elif key in nested_ids:
                setattr(education_program, key + "_id", value.get("id"))
        db.session.commit()
        return get_education_program_response()

    @education_programs_ns.marshal_with(serviced_education_program_model)
    def delete(self, id):
        """Delete the education program with given id"""
        education_program = get_education_program_or_404(id)
        db.session.delete(education_program)
        db.session.commit()
        return get_education_program_response()
