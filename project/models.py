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
    name: str = db.Column(db.String(100), nullable=False)
    position: str = db.Column(db.String(100), nullable=False)
    degree: str = db.Column(db.String(100), nullable=False)
    university: str = db.Column(db.String(100), nullable=False)
    department: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(100), nullable=False, unique=True)
    comments: str = db.Column(db.String(100), nullable=False)


class University(db.Model):
    __tablename__ = "universities"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150), nullable=False)
    abbr: str = db.Column(db.String(45), nullable=False)
    url: str = db.Column(db.String(255), nullable=False)
    programs_list: str = db.Column(db.String(255))

    departments = db.relationship("Department", back_populates="university")


class Department(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    url: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    address: str = db.Column(db.String(255), nullable=False)
    email: str = db.Column(db.String(45), nullable=False)
    phone: str = db.Column(db.String(45), nullable=False)
    university_id = db.Column(db.ForeignKey("universities.id"))

    university = db.relationship("University", back_populates="departments", cascade="all, delete")


class Program(db.Model):
    __tablename__ = "programs"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False)
    specialty_id: int = db.Column(db.ForeignKey("specialty.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    program_link: str = db.Column(db.String(200), nullable=False)
    university_id: int = db.Column(db.ForeignKey("universities.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    level: int = db.Column(db.ForeignKey('programs_level.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    garant: str = db.Column(db.String(100), nullable=False)
    school_name: str = db.Column(db.String(200), nullable=False)
    school_link: str = db.Column(db.String(200), nullable=False)
    clabus_link: str = db.Column(db.String(200), nullable=False)

    specialty = db.relationship(Specialty, backref="program_sp")
    university = db.relationship(University, backref='program_un')
    program_level = db.relationship(ProgramLevel, backref='program_pl')
