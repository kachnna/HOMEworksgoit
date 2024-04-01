from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    phone = Column(String(15), nullable=True)
    birthday = Column(Date, nullable=True)
    notes = Column(String(500), nullable=True)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="tags")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(250), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
