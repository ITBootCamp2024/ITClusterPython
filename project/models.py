from project.extensions import db


class ProgramLevel(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)


class Specialty(db.Model):
    __tablename__ = "specialty"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False)
    link_standart: str = db.Column(db.String(200), nullable=False)
