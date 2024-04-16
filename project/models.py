from datetime import datetime

from project.extensions import db


class Department(db.Model):
    __tablename__ = "department"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    university_id: int = db.Column(db.ForeignKey("university.id"), nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    address: str = db.Column(db.String(255), nullable=False)
    email: str = db.Column(db.String(45), nullable=False)
    phone: str = db.Column(db.String(45), nullable=False)
    url: str = db.Column(db.String(255), nullable=False)

    @property
    def contacts(self):
        return {
            "address": self.address,
            "email": self.email,
            "phone": self.phone.split(", "),
        }

    @contacts.setter
    def contacts(self, value):
        if not value:
            return
        self.address = value.get("address") or self.address
        self.email = value.get("email") or self.email
        phones = value.get("phone")
        if isinstance(phones, list):
            self.phone = ", ".join(phones)
        elif isinstance(phones, str):
            self.phone = phones

    education_programs = db.relationship(
        "EducationProgram", back_populates="department", cascade="all, delete"
    )
    teachers = db.relationship(
        "Teacher", back_populates="department", cascade="all, delete"
    )
    university = db.relationship("University", back_populates="department")


class Discipline(db.Model):
    __tablename__ = "disciplines"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    teacher_id: int = db.Column(db.ForeignKey("teachers.id"), nullable=False)
    discipline_group_id: int = db.Column(db.ForeignKey("discipline_groups.id"), nullable=False)
    education_program_id: int = db.Column(db.ForeignKey("education_programs.id"), nullable=False)
    syllabus_url: str = db.Column(db.String(255))
    education_plan_url: str = db.Column(db.String(255))

    syllabuses = db.relationship(
        "Syllabus", back_populates="discipline", cascade="all, delete"
    )
    teacher = db.relationship("Teacher", back_populates="disciplines")
    discipline_group = db.relationship("DisciplineGroup", back_populates="disciplines")
    education_program = db.relationship(
        "EducationProgram", back_populates="disciplines"
    )

    @property
    def discipline_block(self):
        return self.discipline_group.block


class DisciplineBlock(db.Model):
    __tablename__ = "discipline_blocks"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text)

    disciplineGroups = db.relationship(
        "DisciplineGroup", back_populates="block", cascade="all, delete"
    )


class DisciplineGroup(db.Model):
    __tablename__ = "discipline_groups"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text)
    block_id: int = db.Column(db.ForeignKey("discipline_blocks.id"), nullable=False)
    discipline_url: str = db.Column(db.String(255))

    disciplines = db.relationship(
        "Discipline", back_populates="discipline_group", cascade="all, delete"
    )
    block = db.relationship(
        "DisciplineBlock", back_populates="disciplineGroups"
    )


class EducationLevel(db.Model):
    __tablename__ = "education_levels"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(45), nullable=False)
    education_level: str = db.Column(db.String(45), nullable=False)

    education_programs = db.relationship(
        "EducationProgram", back_populates="education_level", cascade="all, delete"
    )


class EducationProgram(db.Model):
    __tablename__ = "education_programs"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    education_level_id: int = db.Column(
        db.ForeignKey("education_levels.id"), nullable=False
    )
    guarantor: str = db.Column(db.String(100), nullable=False)
    department_id: int = db.Column(db.ForeignKey("department.id"), nullable=False)
    program_url: str = db.Column(db.String(255), nullable=False)
    syllabus_url: str = db.Column(db.String(255), nullable=False)
    specialty_id: str = db.Column(db.ForeignKey("specialty.id"), nullable=False)

    disciplines = db.relationship(
        "Discipline", back_populates="education_program", cascade="all, delete"
    )
    education_level = db.relationship(
        "EducationLevel", back_populates="education_programs"
    )
    department = db.relationship("Department", back_populates="education_programs")
    specialty = db.relationship("Specialty", back_populates="education_programs")

    @property
    def university(self):
        return self.department.university if self.department else None


class Position(db.Model):
    __tablename__ = "position"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text)

    teachers = db.relationship(
        "Teacher", back_populates="position", cascade="all, delete"
    )


class Role(db.Model):
    __tablename__ = "role"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(45), nullable=False)

    teachers = db.relationship("Teacher", back_populates="role", cascade="all, delete")
    users = db.relationship("User", back_populates="role", cascade="all, delete")


class Specialty(db.Model):
    __tablename__ = "specialty"
    id: int = db.Column(db.Integer, primary_key=True)
    code: str = db.Column(db.String(45), nullable=False)
    name: str = db.Column(db.String(100), nullable=False)
    standard_url: str = db.Column(db.String(255))

    education_programs = db.relationship(
        "EducationProgram", back_populates="specialty", cascade="all, delete"
    )


class Syllabus(db.Model):
    __tablename__ = "syllabuses"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    status: str = db.Column(db.String(45), nullable=False)
    discipline_id: int = db.Column(db.ForeignKey("disciplines.id"), nullable=False)

    discipline = db.relationship("Discipline", back_populates="syllabuses")

    def teacher(self):
        return self.discipline.teacher if self.discipline else None


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    position_id: int = db.Column(db.ForeignKey("position.id"), nullable=False)
    email: str = db.Column(db.String(100), nullable=False, unique=True)
    department_id: int = db.Column(db.ForeignKey("department.id"), nullable=False)
    comments: str = db.Column(db.Text)
    degree_level = db.Column(db.String(50))
    role_id = db.Column(db.ForeignKey("role.id"), nullable=False)

    disciplines = db.relationship(
        "Discipline", back_populates="teacher", cascade="all, delete"
    )
    position = db.relationship("Position", back_populates="teachers")
    department = db.relationship("Department", back_populates="teachers")
    role = db.relationship("Role", back_populates="teachers")

    @property
    def university(self):
        return self.department.university if self.department else None


class University(db.Model):
    __tablename__ = "university"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(150), nullable=False)
    abbr: str = db.Column(db.String(45), nullable=False)
    programs_list_url: str = db.Column(db.String(255), nullable=False)
    url: str = db.Column(db.String(255), nullable=False)

    department = db.relationship(
        "Department", back_populates="university", cascade="all, delete"
    )


class User(db.Model):
    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(100), nullable=False)
    last_name: str = db.Column(db.String(100), nullable=False)
    parent_name: str = db.Column(db.String(100))
    email: str = db.Column(db.String(100), unique=True)
    password_hash: str = db.Column(db.String(255), nullable=False)
    phone: str = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow())
    role_id: int = db.Column(db.ForeignKey("role.id"), nullable=False)
    email_confirmed: bool = db.Column(db.Boolean, default=False, nullable=False)
    active_status: bool = db.Column(db.Boolean, default=True, nullable=False)

    role = db.relationship("Role", back_populates="users")
