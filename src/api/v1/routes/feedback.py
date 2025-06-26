from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import FeedbackModel, InterviewModel, get_db
from src.schemas.feedback import (
    FeedbackCreate,
    FeedbackCreateData,
    FeedbackCreateResponse,
    FeedbackViewResponse,
)

feedback_router = APIRouter()


@feedback_router.post("", response_model=FeedbackCreateResponse, status_code=201)
async def submit_feedback(
    interview_id: int, feedback_data: FeedbackCreate, db: AsyncSession = Depends(get_db)
):

    interview_query_result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.id == interview_id)
        .options(selectinload(InterviewModel.feedback))  # preload ก่อน!
    )
    interview = interview_query_result.scalars().first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.feedback:
        raise HTTPException(status_code=400, detail="Feedback already exists")

    # use model_dump instead .dict()
    feedback = FeedbackModel(interview_id=interview_id, **feedback_data.model_dump())

    db.add(feedback)

    await db.commit()
    await db.refresh(feedback)

    result = {
        "status": True,
        "message": "Feedback submitted successfully",
        "data": FeedbackCreateData.model_validate(feedback),
    }

    return result


@feedback_router.get("", response_model=FeedbackViewResponse)
async def view_feedback(interview_id: int, db: AsyncSession = Depends(get_db)):
    feedback_query_result = await db.execute(
        select(FeedbackModel).where(FeedbackModel.interview_id == interview_id)
    )
    feedback = feedback_query_result.scalars().first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    result = {
        "status": True,
        "message": "Feedback retrieved successfully",
        "data": feedback,
    }
    return result
