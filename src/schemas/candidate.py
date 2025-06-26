import datetime
import enum

from pydantic import BaseModel
from typing import List, Optional


class CandidateStatusEnum(str, enum.Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    HIRED = "hired"
    REJECTED = "rejected"


class CandidateCreate(BaseModel):
    name: str
    email: str
    position: str
    status: CandidateStatusEnum


class CandidateStatusUpdate(BaseModel):
    status: CandidateStatusEnum

class CandidateCreateDataResponse(BaseModel):
    id: str
    name: str
    email: str
    position: str
    status: CandidateStatusEnum

    class Config:
        from_attributes = True

class CandidateCreateResponse(BaseModel):
    status: bool
    message: str
    data: CandidateCreateDataResponse


class FeedbackResponse(BaseModel):
    id: int
    interview_id: int
    rating: int
    comment: str

class InterviewResponse(BaseModel):
    id: int
    candidate_id: str
    interviewer: str
    scheduled_at: datetime.datetime  # ISO format datetime string
    result: Optional[str]
    feedback: Optional[FeedbackResponse]

 
class CandidateListDataResponse(BaseModel):
    id: str
    name: str
    email: str
    position: str
    status: CandidateStatusEnum
    interviews: List[InterviewResponse] = []



class CandidateListResponse(BaseModel):
    status: bool
    message: str
    data: List[CandidateListDataResponse]