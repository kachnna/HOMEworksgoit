from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey(
        'groups.id', onupdate="CASCADE", ondelete="CASCADE"))
    group = relationship('Group', passive_updates=True, passive_deletes=True)


class Lecturer(Base):
    __tablename__ = 'lecturers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    lecturer_id = Column(Integer, ForeignKey(
        'lecturers.id', onupdate="CASCADE", ondelete="CASCADE"))
    lecturer = relationship(
        'Lecturer', passive_updates=True, passive_deletes=True)


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grades = Column(String)
    student_id = Column(Integer, ForeignKey(
        'students.id', onupdate="CASCADE", ondelete="CASCADE"))
    student = relationship(
        'Student', passive_updates=True, passive_deletes=True)
    subject_id = Column(Integer, ForeignKey(
        'subjects.id', onupdate="CASCADE", ondelete="CASCADE"))
    subject = relationship(
        'Subject', passive_updates=True, passive_deletes=True)
    created_at = Column(Date)
