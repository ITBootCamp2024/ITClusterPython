from project.extensions import db


class Degree(db.Model):
    __tablename__ = "degree"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(45), nullable=False)

    teachers = db.relationship("Teacher", back_populates="degree", cascade="all, delete")


class Department(db.Model):
    __tablename__ = "department"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    university_id: int = db.Column(db.ForeignKey("university.id"))
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
            "phone": self.phone.split(", ")
        }

    @contacts.setter
    def contacts(self, value):
        if not value:
            return
        self.address = value.get("address") or self.address
        self.email = value.get("email") or self.email
        if value.get("phone") and isinstance(value.get("phone"), list):
            self.phone = ", ".join(value.get("phone"))

    education_programs = db.relationship("EducationProgram", back_populates="department", cascade="all, delete")
    teachers = db.relationship("Teacher", back_populates="department", cascade="all, delete")
    university = db.relationship("University", back_populates="department")


class DisciplineBlock(db.Model):
    __tablename__ = "discipline_blocks"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    description: str = db.Column(db.Text)

    discipline_groups = db.relationship("DisciplineGroup", back_populates="block", cascade="all, delete")


class DisciplineGroup(db.Model):
    __tablename__ = "discipline_groups"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text)
    block_id: int = db.Column(db.ForeignKey("discipline_blocks.id"))
    discipline_url: str = db.Column(db.String(255))

    block = db.relationship("DisciplineBlock", back_populates="discipline_groups")


class EducationLevel(db.Model):
    __tablename__ = "education_levels"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(45), nullable=False)

    education_programs = db.relationship("EducationProgram", back_populates="education_level", cascade="all, delete")


class EducationProgram(db.Model):
    __tablename__ = "education_programs"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    education_level_id: int = db.Column(db.ForeignKey("education_levels.id"), nullable=True)
    guarantor: str = db.Column(db.String(100), nullable=False)
    department_id: int = db.Column(db.ForeignKey("department.id"), nullable=True)
    program_url: str = db.Column(db.String(255), nullable=False)
    syllabus_url: str = db.Column(db.String(255), nullable=False)
    specialty_id: str = db.Column(db.ForeignKey("specialty.id"), nullable=True)

    education_level = db.relationship("EducationLevel", back_populates="education_programs")
    department = db.relationship("Department", back_populates="education_programs")
    specialty = db.relationship("Specialty", back_populates="education_programs")

    @property
    def university(self):
        return self.department.university if self.department else None


class Position(db.Model):
    __tablename__ = "position"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)

    teachers = db.relationship("Teacher", back_populates="position", cascade="all, delete")


class Specialty(db.Model):
    __tablename__ = "specialty"
    id: int = db.Column(db.Integer, primary_key=True)
    code: str = db.Column(db.String(45), nullable=False)
    name: str = db.Column(db.String(100), nullable=False)
    standard_url: str = db.Column(db.String(255))

    education_programs = db.relationship("EducationProgram", back_populates="specialty", cascade="all, delete")


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    position_id: int = db.Column(db.ForeignKey("position.id"), nullable=True)
    degree_id: int = db.Column(db.ForeignKey("degree.id"), nullable=True)
    email: str = db.Column(db.String(100), nullable=False, unique=True)
    department_id: int = db.Column(db.ForeignKey("department.id"))
    comments: str = db.Column(db.Text)

    position = db.relationship("Position", back_populates="teachers")
    degree = db.relationship("Degree", back_populates="teachers")
    department = db.relationship("Department", back_populates="teachers")

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

    department = db.relationship("Department", back_populates="university", cascade="all, delete")
