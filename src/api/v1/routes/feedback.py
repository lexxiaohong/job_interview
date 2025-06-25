from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import enum
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database import CandidateModel, FeedbackModel, InterviewModel, get_db
import datetime

feedback_router = APIRouter()




class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str]

class FeedbackResponse(BaseModel):
    id: int
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True



@feedback_router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    interview_id: int,
    feedback_data: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.id == interview_id)
        .options(selectinload(InterviewModel.feedback))  # preload ก่อน!
    )
    interview = result.scalars().first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.feedback:
        raise HTTPException(status_code=400, detail="Feedback already exists")

    feedback = FeedbackModel(interview_id=interview_id, **feedback_data.dict())
    

    feedback = FeedbackModel(interview_id=interview_id, **feedback_data.dict())
    db.add(feedback)

    await db.commit()

    return feedback


# @feedback_router.get("", response_model=FeedbackResponse)
# async def view_feedback(
#     interview_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(select(FeedbackModel).where(FeedbackModel.interview_id == interview_id))
#     feedback = result.scalars().first()
#     if not feedback:
#         raise HTTPException(status_code=404, detail="Feedback not found")
#     return feedback
