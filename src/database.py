# src/database.py

import uuid
from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime
import enum

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class CandidateStatus(str, enum.Enum):
    applied = "applied"
    interviewing = "interviewing"
    hired = "hired"
    rejected = "rejected"

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    status = Column(Enum(CandidateStatus), nullable=False)

    # relationship: One Candidate -> Many Interviews
    interviews = relationship("Interview", back_populates="candidate")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    interviewer = Column(String, nullable=False)
    scheduled_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    result = Column(String, nullable=True)

    # relationships
    candidate = relationship("Candidate", back_populates="interviews")
    feedbacks = relationship("Feedback", back_populates="interview")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)

    interview = relationship("Interview", back_populates="feedbacks")