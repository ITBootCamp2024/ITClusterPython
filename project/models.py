from project.extensions import db


class ProgramLevel(db.Model):
    __tablename__ = "programs_level"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)


class Specialty(db.Model):
    __tablename__ = "specialty"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name: str = db.Column(db.String(200), nullable=False)
    link_standart: str = db.Column(db.String(200), nullable=False)


class CourseBlocks(db.Model):
    __tablename__ = "course_blocks"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text, nullable=False)


class CourseStatuses(db.Model):
    __tablename__ = "course_statuses"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text, nullable=False)


class CourseGroupes(db.Model):
    __tablename__ = "course_groupes"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    # TODO: Дописати зв'язок
    type_id: int = db.Column(db.Integer, nullable=False)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    role: str = db.Column(db.String(50), nullable=False)
    status: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(100), nullable=False, unique=True)
    details: str = db.Column(db.Text, nullable=False)


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
