from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# docker run --name school -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres
engine = create_engine('sqlite:///school.db')
Session = sessionmaker(bind=engine)
session = Session()
