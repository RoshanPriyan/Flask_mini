from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

baseurl = f"{DATABASE_URL}://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"

try:
    engine = create_engine(baseurl, echo=False)
except Exception as e:
    raise ConnectionError(f"Failed to connect to the database: {e}")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
