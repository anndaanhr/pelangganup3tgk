from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Hardcode untuk testing cepat - pastikan database dan user sudah dibuat
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Check if connection is still alive
    pool_recycle=300,        # Recycle connections every 5 minutes
    pool_timeout=10,         # Don't wait forever if pool is exhausted (throw error)
    max_overflow=10          # Allow 10 extra connections
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency untuk mendapatkan database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

