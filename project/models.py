from project.extensions import db


class ProgramLevel(db.Model):
    __tablename__ = "programs_level"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)


class Specialty(db.Model):
    __tablename__ = "specialty"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False)
    link_standart: str = db.Column(db.String(200), nullable=False)

      
class CourseBlocks(db.Model):
    __tablename__ = "course_blocks"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
