import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import CandidateModel, InterviewModel, get_db

interview_router = APIRouter()


class InterviewCreate(BaseModel):
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str]


@interview_router.post("/")
async def create_schedule_interview(
    candidate_id: str, interview: InterviewCreate, db: AsyncSession = Depends(get_db)
):
    # Check candidate exist
    result = await db.execute(
        select(CandidateModel).where(CandidateModel.id == candidate_id)
    )

    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Create interview
    db_interview = InterviewModel(
        candidate_id=candidate_id,
        interviewer=interview.interviewer,
        scheduled_at=interview.scheduled_at,
        result=interview.result,
    )
    db.add(db_interview)
    await db.commit()
    await db.refresh(db_interview)

    return db_interview


@interview_router.get("")
async def list_candidate_interviews(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == id))
    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.candidate_id == id)
        .options(selectinload(InterviewModel.feedback))  # preload feedback
    )
    results = result.scalars().all()
    print("results:", results)
    return results
