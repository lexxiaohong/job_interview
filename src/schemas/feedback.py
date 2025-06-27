from typing import Optional
from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    rating:  int = Field(..., ge=1, le=5)
    comment: str


class FeedbackCreateData(BaseModel):
    id: int
    rating: int
    comment: str

    class Config:
        from_attributes = True


class FeedbackCreateResponse(BaseModel):
    status: bool
    message: str
    data: Optional[FeedbackCreateData] = None


class FeedbackViewData(BaseModel):
    id: int
    interview_id: int
    rating: int
    comment: str


class FeedbackViewResponse(BaseModel):
    status: bool
    message: str
    data: Optional[FeedbackViewData] = None
