import datetime
import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.database import Base


class CandidateStatus(str, enum.Enum):
    applied = "applied"
    interviewing = "interviewing"
    hired = "hired"
    rejected = "rejected"


class CandidateModel(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    status = Column(Enum(CandidateStatus), nullable=False)

    interviews = relationship(
        "InterviewModel",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )


class InterviewModel(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(String, ForeignKey("candidates.id"), nullable=False)
    interviewer = Column(String, nullable=False)
    scheduled_at = Column(DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    result = Column(String, nullable=True)

    # relationships
    candidate = relationship("CandidateModel", back_populates="interviews")
    feedback = relationship(
        "FeedbackModel",
        back_populates="interview",
        uselist=False,
        cascade="all, delete-orphan",
    )


class FeedbackModel(Base):
    __tablename__ = "feedbacks"
    __table_args__ = (
        UniqueConstraint("interview_id", name="uq_feedback_interview_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)

    interview = relationship("InterviewModel", back_populates="feedback")
