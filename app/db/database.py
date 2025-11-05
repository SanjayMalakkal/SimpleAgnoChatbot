from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./user_steps.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
