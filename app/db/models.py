import enum
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

class Role(enum.Enum):
    student = enum.auto()
    teacher = enum.auto()
    admin = enum.auto()
    editor = enum.auto()

Base = declarative_base()

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String)
    classes = relationship("Class", back_populates="school")

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    school = relationship("School", back_populates="classes")
    students = relationship("Student", back_populates="student_class")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    student_class = relationship("Class", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    courses = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)