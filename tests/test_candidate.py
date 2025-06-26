# tests/unit/test_create_candidate_with_db.py
from unittest.mock import AsyncMock, MagicMock
import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import CandidateModel
from src.schemas.candidate import CandidateCreate, CandidateCreateDataResponse
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

    
@pytest.mark.asyncio
async def test_create_candidate_with_mock():
    # Arrange
    mock_db = AsyncMock()

    candidate_data = CandidateCreate(
        name="Mock User",
        email="mock@example.com",
        position="Python Developer",
        status="applied"
    )

    # จำลองว่าไม่มี email ซ้ำ
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # จำลอง model หลังถูก refresh
    mock_candidate_model = CandidateModel(
        id="mock-id",
        name="Mock User",
        email="mock@example.com",
        position="Python Developer",
        status="applied"
    )
    mock_db.refresh.side_effect = lambda obj: setattr(obj, "id", "mock-id")  # set id manually
  
    # Act
    result = await create_candidate(candidate=candidate_data, db=mock_db)

    # Assert
    assert result.status is True
    assert result.message == "Candidate created successfully"
    assert isinstance(result.data, CandidateCreateDataResponse)
    assert result.data.email == "mock@example.com"
    assert result.data.name == "Mock User"

    mock_db.execute.assert_awaited_once()
    mock_db.add.assert_called_once()
    # ตรวจสอบว่าถูกเรียก .add() และ object ที่ add มีค่าถูกต้อง
    added_obj = mock_db.add.call_args[0][0]
    assert added_obj.id == "mock-id"
    assert added_obj.name == "Mock User"
    assert added_obj.email == "mock@example.com"
    assert added_obj.position == "Python Developer"
    assert added_obj.status == "applied"
    
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()
    refresh_obj = mock_db.refresh.call_args[0][0]
    assert refresh_obj.id == "mock-id"
    assert refresh_obj.name == "Mock User"
    assert refresh_obj.email == "mock@example.com"
    assert refresh_obj.position == "Python Developer"
    assert refresh_obj.status == "applied"
    

