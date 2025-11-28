from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# IMPORTANT:
# Fill in your PostgreSQL username, password, and database name
#DATABASE_URL = "postgresql://shamar:Shamsean%4021@localhost:5432/portfolio"

# SQLAlchemy engine (connect to PostgreSQL)
engine = create_engine(DATABASE_URL)

# SessionLocal will be used to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for model definitions
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()