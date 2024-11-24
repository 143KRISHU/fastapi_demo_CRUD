# Manages database sessions.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #type : ignore
