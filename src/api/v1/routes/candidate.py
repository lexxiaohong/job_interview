from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import enum
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database import CandidateModel, InterviewModel, get_db
import datetime

candidate_router = APIRouter()

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

class InterviewCreate(BaseModel):
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str]

@candidate_router.post("/")
async def create_candidate(candidate: CandidateCreate, db: AsyncSession = Depends(get_db)):
    db_candidate = CandidateModel(
        name=candidate.name,
        email=candidate.email,
        position=candidate.position,
        status=candidate.status,
    )
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate


@candidate_router.get("/")
async def list_candidates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CandidateModel).options(selectinload(CandidateModel.interviews).selectinload(InterviewModel.feedback))
    )

    candidates = result.scalars().all()
    return candidates


@candidate_router.patch("/{id}")
async def update_candidate_status(id: str, status_update: CandidateStatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == id))
    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.status = status_update.status
    await db.commit()

    return candidate


@candidate_router.delete("/{id}", status_code=204)
async def delete_candidate(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == id))
    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    await db.delete(candidate)
    await db.commit()

    return  # No content response (204 No Content)


@candidate_router.post("/{id}/interviews")
async def create_schedule_interview(id: str, interview: InterviewCreate, db: AsyncSession = Depends(get_db)):
    # Check candidate exist
    print("id:", id)
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == id))
    print("result:", result)
    candidate = result.scalars().first()
    print("candidate:", candidate)

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Create interview
    db_interview = InterviewModel(
        candidate_id=id,
        interviewer=interview.interviewer,
        scheduled_at=interview.scheduled_at,
        result=interview.result
    )
    db.add(db_interview)
    await db.commit()
    await db.refresh(db_interview)

    return db_interview



