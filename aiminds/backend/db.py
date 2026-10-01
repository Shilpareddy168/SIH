"""PostgreSQL via SQLAlchemy. Falls back to SQLite so you can start without installing Postgres."""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# Postgres example: postgresql://postgres:pass@localhost:5432/aiminds
URL = os.getenv("DATABASE_URL", "sqlite:///./aiminds.db")
engine = create_engine(URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    user = Column(String, index=True)
    kind = Column(String)            # "assessment" or "quiz"
    score = Column(Integer)
    total = Column(Integer)
    created = Column(DateTime, server_default=func.now())

Base.metadata.create_all(engine)
