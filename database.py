from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


def create_db_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_DATABASE")

    try:
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    except Exception as e:
        print("Error:", e)
        engine = None

    return engine
