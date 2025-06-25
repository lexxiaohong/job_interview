from fastapi import APIRouter, Depends
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


