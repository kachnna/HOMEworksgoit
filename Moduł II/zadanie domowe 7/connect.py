from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


# POSTGRES_ADDRESS = 'localhost'
# POSTGRES_PORT = '5432'
# POSTGRES_USERNAME = 'postgres'
# POSTGRES_PASSWORD = '1234'
# POSTGRES_DBNAME = 'postgres'


# DATABASE_URL = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:{POSTGRES_PORT}/{POSTGRES_DBNAME}'
# print(DATABASE_URL)
# engine = create_engine(DATABASE_URL)
# docker run --name school -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres
engine = create_engine('sqlite:///school.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
