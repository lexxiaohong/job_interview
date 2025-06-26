import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.interview import (
    CandiateInterviewListResponse,
    InterviewCreate,
    InterviewCreateData,
    InterviewCreateResponse,
)
from src.database import CandidateModel, InterviewModel, get_db

interview_router = APIRouter()


@interview_router.post("", response_model=InterviewCreateResponse, status_code=201)
async def create_schedule_interview(
    candidate_id: str, interview: InterviewCreate, db: AsyncSession = Depends(get_db)
):
    # Check candidate exist
    candidate_query_result = await db.execute(
        select(CandidateModel).where(CandidateModel.id == candidate_id)
    )

    candidate = candidate_query_result.scalars().first()

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
    
    
    result = {
        "status": True,
        "message": "Interview scheduled successfully",
        "data": InterviewCreateData.model_validate(db_interview),
    }

    return result


@interview_router.get("", response_model=CandiateInterviewListResponse)
async def list_candidate_interviews(
    candidate_id: str, db: AsyncSession = Depends(get_db)
):
    candidate_query_result = await db.execute(
        select(CandidateModel).where(CandidateModel.id == candidate_id)
    )
    candidate = candidate_query_result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    interview_query_result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.candidate_id == candidate_id)
        .options(selectinload(InterviewModel.feedback))  # preload feedback
    )
    interview_results = interview_query_result.scalars().all()

    result = {
        "status": True,
        "message": "Interviews retrieved successfully",
        "data": interview_results,
    }
    return result
