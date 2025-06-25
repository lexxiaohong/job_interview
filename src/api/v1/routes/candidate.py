from fastapi import APIRouter, Depends, HTTPException
import enum
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database import CandidateModel, get_db

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
        select(CandidateModel).options(selectinload(CandidateModel.interviews))
    )
    candidates = result.scalars().all()
    return candidates


@candidate_router.patch("/{candidate_id}")
async def update_candidate_status(candidate_id: str, status_update: CandidateStatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == candidate_id))
    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.status = status_update.status
    await db.commit()

    return candidate


