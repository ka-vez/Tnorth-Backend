import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABSE_URL = "sqlite:///tnorth.db"
 
# engine = create_engine(SQLALCHEMY_DATABSE_URL, connect_args={'check_same_thread': False})

load_dotenv()

SQLALCHEMY_DATABSE_URL = os.getenv("DATABASE_URL")
 
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()