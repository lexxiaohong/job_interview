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

class CandidateResponse(BaseModel):
    id: str
    name: str
    email: str
    position: str
    status: CandidateStatusEnum


class InterviewResponse(BaseModel):
    id: int
    candidate_id: str
    interviewer: str
    scheduled_at: datetime.datetime  # ISO format datetime string
    result: Optional[str]

 
class CandidatelistdetailResponse(BaseModel):
    id: str
    name: str
    email: str
    position: str
    status: CandidateStatusEnum
    interviews: List[InterviewResponse] = []



class CandidateListResponse(BaseModel):
    status: bool
    message: str
    data: List[CandidatelistdetailResponse]