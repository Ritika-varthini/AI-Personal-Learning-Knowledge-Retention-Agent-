from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite file
SQLITE_URL = "sqlite:///./data/kb.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables when this file is imported
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
