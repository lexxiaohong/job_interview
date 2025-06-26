from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.candidate import (
    CandidateCreate,
    CandidateCreateDataResponse,
    CandidateListResponse,
    CandidateCreateResponse,
    CandidateStatusUpdate,
)
from src.database import CandidateModel, InterviewModel, get_db

candidate_router = APIRouter()


@candidate_router.post("/", response_model=CandidateCreateResponse, status_code=201)
async def create_candidate(
    candidate: CandidateCreate, db: AsyncSession = Depends(get_db)
):
    # check existing email
    candidate_query_result = await db.execute(
        select(CandidateModel).where(CandidateModel.email == candidate.email)
    )
    existing_candidate = candidate_query_result.scalars().first()
    if existing_candidate:
        raise HTTPException(
            status_code=400, detail="Candidate with this email already exists"
        )

    db_candidate = CandidateModel(
        name=candidate.name,
        email=candidate.email,
        position=candidate.position,
        status=candidate.status,
    )
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)

    result = CandidateCreateResponse(
        status=True,
        message="Candidate created successfully",
        data=CandidateCreateDataResponse.model_validate(db_candidate),
    )

    return result


@candidate_router.get("/", response_model=CandidateListResponse)
async def list_candidates(db: AsyncSession = Depends(get_db)):
    candidate_query_result = await db.execute(
        select(CandidateModel).options(
            selectinload(CandidateModel.interviews).selectinload(
                InterviewModel.feedback
            )
        )
    )

    candidates = candidate_query_result.scalars().all()
    result = {
        "status": True,
        "message": "Candidates retrieved successfully",
        "data": candidates,
    }

    return result


@candidate_router.patch("/{id}", response_model=CandidateCreateResponse)
async def update_candidate_status(
    id: str, status_update: CandidateStatusUpdate, db: AsyncSession = Depends(get_db)
):
    candidate_query_result = await db.execute(
        select(CandidateModel).where(CandidateModel.id == id)
    )
    candidate = candidate_query_result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.status = status_update.status
    await db.commit()
    await db.refresh(candidate)

    result = {
        "status": True,
        "message": "Candidate status updated successfully",
        "data": candidate,
    }

    return result


@candidate_router.delete("/{id}", status_code=204)
async def delete_candidate(id: str, db: AsyncSession = Depends(get_db)):
    candidate_query_result = await db.execute(
        select(CandidateModel).where(CandidateModel.id == id)
    )
    candidate = candidate_query_result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    await db.delete(candidate)
    await db.commit()

    return  # No content response (204 No Content)
