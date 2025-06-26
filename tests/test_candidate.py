# tests/unit/test_create_candidate_with_db.py
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.candidate import CandidateCreate
from src.api.v1.routes.candidate import create_candidate


@pytest.mark.asyncio
async def test_create_candidate_success_with_db(db_session: AsyncSession):
    print("db_session:", db_session)
    candidate_data = CandidateCreate(
        name="Hengheng",
        email="Hengheng@example.com",
        position="Tester",
        status="applied",
    )
    print("candidate_data:", candidate_data)

    result = await create_candidate(candidate=candidate_data, db=db_session)
    print("Result:", result)
    # assert result["status"] is True
    # assert result["data"].email == candidate_data.email
    # assert result["data"].name == candidate_data.name

    # # ดึงจาก DB จริงเพื่อตรวจสอบอีกครั้ง
    # from src.models.models import CandidateModel
    # query_result = await db_session.execute(
    #     select(CandidateModel).where(CandidateModel.email == candidate_data.email)
    # )
    # db_candidate = query_result.scalars().first()
    # assert db_candidate is not None
    # assert db_candidate.name == candidate_data.name
