# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database connection configuration using your provided information
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'wsl15253021368'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'osgraph'

DATABASE_URL = f"mysql+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"

# Create the engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Session management
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# For FastAPI dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()