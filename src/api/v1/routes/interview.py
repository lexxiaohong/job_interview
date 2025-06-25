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

interview_router = APIRouter()



class InterviewCreate(BaseModel):
    interviewer: str
    scheduled_at: datetime.datetime
    result: Optional[str]


@interview_router.post("/")
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


@interview_router.get("")
async def list_candidate_interviews(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    # ตรวจสอบว่าผู้สมัครมีอยู่จริง
    result = await db.execute(select(CandidateModel).where(CandidateModel.id == id))
    candidate = result.scalars().first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # ดึงรายการสัมภาษณ์ทั้งหมดของ candidate id นี้
 
    result = await db.execute(
        select(InterviewModel)
        .where(InterviewModel.candidate_id == id)
        .options(selectinload(InterviewModel.feedback))  # preload feedback
    )
    results = result.scalars().all()
    print("results:", results)
    return results



