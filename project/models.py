from sqlalchemy import UniqueConstraint

from project.extensions import db


class University(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False, unique=True)
    shortname: str = db.Column(db.String(20), nullable=False, unique=True)
    sitelink: str = db.Column(db.String(100), nullable=False)
    programs_list: str = db.Column(db.String(200), nullable=False)
    schools = db.relationship("School", back_populates="university")


class School(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False, unique=True)
    size: str = db.Column(db.Integer, nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    contact: str = db.Column(db.String(100), nullable=False)
    university_id = db.Column(db.ForeignKey("university.id"))

    university = db.relationship("University", back_populates="schools", cascade="all, delete")
