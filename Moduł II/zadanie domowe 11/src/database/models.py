from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    birthday = Column(Date, nullable=True)
    notes = Column(String(500), nullable=True)
