# src/database.py

import uuid
from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import datetime
import enum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./test.db"



engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session




class CandidateStatus(str, enum.Enum):
    applied = "applied"
    interviewing = "interviewing"
    hired = "hired"
    rejected = "rejected"

class CandidateModel(Base):
    __tablename__ = "candidates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    status = Column(Enum(CandidateStatus), nullable=False)

    # relationship: One Candidate -> Many Interviews
    interviews = relationship("InterviewModel", back_populates="candidate")

class InterviewModel(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    interviewer = Column(String, nullable=False)
    scheduled_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    result = Column(String, nullable=True)

    # relationships
    candidate = relationship("CandidateModel", back_populates="interviews")
    feedbacks = relationship("FeedbackModel", back_populates="interview")

class FeedbackModel(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)

    interview = relationship("InterviewModel", back_populates="feedbacks")