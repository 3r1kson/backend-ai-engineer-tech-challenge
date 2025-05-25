# python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

def get_open_ai_key():
    return os.getenv("OPEN_AI_KEY")

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# INSTANCE_DIR = os.path.join(BASE_DIR, "../instance")
#
# if not os.path.exists(INSTANCE_DIR):
#     os.makedirs(INSTANCE_DIR)
#
# DATABASE_PATH = os.path.join(INSTANCE_DIR, "tech_challenge.db")
# DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
#
# engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()


