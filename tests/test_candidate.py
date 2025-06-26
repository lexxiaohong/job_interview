# tests/unit/test_create_candidate_with_db.py
import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.candidate import CandidateCreate
from src.api.v1.routes.candidate import create_candidate


@pytest.mark.asyncio
async def test_create_candidate_success_with_db(db_session: AsyncSession):
    candidate_data = CandidateCreate(
        name="Hengheng",
        email="Hengheng@example.com",
        position="Tester",
        status="applied",
    )

    result = await create_candidate(candidate=candidate_data, db=db_session)
    data = result.data
    data_dict = data.model_dump()

    print("Data dict:", data_dict)
    assert result.status is True
    assert result.message == "Candidate created successfully"
    assert data.id is not None
    assert data.name == candidate_data.name
    assert data.email == candidate_data.email
    assert data.position == candidate_data.position
    assert data.status == candidate_data.status

    # pull candidate from unittest db
    from src.models.models import CandidateModel
    query_result = await db_session.execute(
        select(CandidateModel).where(CandidateModel.email == candidate_data.email)
    )
    db_candidate = query_result.scalars().first()

    assert db_candidate is not None
    assert db_candidate.name == candidate_data.name
    assert db_candidate.email == candidate_data.email
    assert db_candidate.position == candidate_data.position
    assert db_candidate.status == candidate_data.status

    
   
