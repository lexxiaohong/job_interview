import datetime
from typing import Optional

from pydantic import BaseModel


class InterviewCreate(BaseModel):
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str] = None


class InterviewCreateData(BaseModel):
    id: int
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str] = None
    candidate_id: str

    class Config:
        from_attributes = True


class InterviewCreateResponse(BaseModel):
    status: bool
    message: str
    data: Optional[InterviewCreateData] = None


class FeedbackResponse(BaseModel):
    id: int
    interview_id: int
    rating: int
    comment: str


class InterviewListData(BaseModel):
    id: int
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str] = None
    candidate_id: str
    feedback: Optional[FeedbackResponse] = None


class CandiateInterviewListResponse(BaseModel):
    status: bool
    message: str
    data: list[InterviewListData]
