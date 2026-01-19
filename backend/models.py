"""
Job Aggregator - Database Models
SQLAlchemy models for PostgreSQL (Supabase)
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Text, BigInteger, 
    DateTime, Boolean, Index, ForeignKey, create_engine
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import DATABASE_URL

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Job(Base):
    """
    Model untuk menyimpan data lowongan kerja
    """
    __tablename__ = "jobs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    salary_min = Column(BigInteger, nullable=True)
    salary_max = Column(BigInteger, nullable=True)
    apply_url = Column(String(500), nullable=False)
    source = Column(String(100), nullable=True)  # Job source (e.g., "stackoverflow", "linkedin")
    
    # AI-processed fields
    skills = Column(JSONB, nullable=True)  # Array of skills extracted by AI
    experience_level = Column(String(50), nullable=True)  # junior, mid, senior
    is_remote = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Create index on created_at for efficient sorting
    __table_args__ = (
        Index('idx_jobs_created_at', 'created_at'),
        Index('idx_jobs_salary', 'salary_min', 'salary_max'),
        Index('idx_jobs_location', 'location'),
    )
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "apply_url": self.apply_url,
            "source": self.source,
            "skills": self.skills,
            "experience_level": self.experience_level,
            "is_remote": self.is_remote,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class UserPreference(Base):
    """
    Model untuk menyimpan preferensi pencarian user
    """
    __tablename__ = "users_preferences"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, unique=True, index=True)
    
    # Search preferences
    keywords = Column(JSONB, nullable=True)  # Array of search keywords
    preferred_locations = Column(JSONB, nullable=True)  # Array of preferred locations
    min_salary = Column(BigInteger, nullable=True)
    max_salary = Column(BigInteger, nullable=True)
    experience_levels = Column(JSONB, nullable=True)  # ["junior", "mid", "senior"]
    remote_only = Column(Boolean, default=False)
    
    # Notification settings
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserPreference(user_id='{self.user_id}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "keywords": self.keywords,
            "preferred_locations": self.preferred_locations,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "experience_levels": self.experience_levels,
            "remote_only": self.remote_only,
            "email_notifications": self.email_notifications,
            "push_notifications": self.push_notifications,
        }


# Database utility functions
def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Create tables when running this file directly
    print("Creating database tables...")
    init_db()
    print("Tables created successfully!")
