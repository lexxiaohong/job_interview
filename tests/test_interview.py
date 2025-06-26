import pytest
from unittest.mock import AsyncMock, MagicMock
import datetime
from src.api.v1.routes.interview import create_schedule_interview
from src.models.models import CandidateModel, InterviewModel
from src.schemas.interview import InterviewCreate
from src.schemas.interview import InterviewCreateData

# python -m pytest tests/test_interview.py

@pytest.mark.asyncio
async def test_create_schedule_interview_success_with_mock():
    candidate_id = "mock-candidate-id"

    interview_data = InterviewCreate(
        interviewer="Mock Interviewer",
        scheduled_at=datetime.datetime(2025, 7, 1, 15, 0),
        result="PASS"
    )

    mock_db = AsyncMock()
    
    # simulate: candidate exists
    mock_candidate = CandidateModel(
        id=candidate_id,
        name="Mock User",
        email="mock@example.com",
        position="Python Developer",
        status="applied"
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_candidate
    mock_db.execute.return_value = mock_result

    # simulate commit & refresh
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()

    # Mock refresh to assign ID
    async def mock_refresh(obj):
        obj.id = 99999
    mock_db.refresh.side_effect = mock_refresh

    result = await create_schedule_interview(candidate_id=candidate_id, interview=interview_data, db=mock_db)

    assert result["status"] is True
    assert result["message"] == "Interview scheduled successfully"
    assert isinstance(result["data"], InterviewCreateData)
    assert result["data"].interviewer == "Mock Interviewer"
    assert result["data"].result == "PASS"
    assert result["data"].candidate_id == candidate_id
    assert result["data"].scheduled_at == datetime.datetime(2025, 7, 1, 15, 0)

    mock_db.execute.assert_awaited_once()
    mock_db.add.assert_called_once()
    add_obj = mock_db.add.call_args[0][0]
    assert isinstance(add_obj, InterviewModel)
    assert add_obj.candidate_id == candidate_id
    assert add_obj.interviewer == interview_data.interviewer
    assert add_obj.scheduled_at == interview_data.scheduled_at
    assert add_obj.result == interview_data.result
    
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()
    refresh_obj = mock_db.refresh.call_args[0][0]
    assert refresh_obj.id == 99999
    assert refresh_obj.candidate_id == candidate_id
    assert refresh_obj.interviewer == interview_data.interviewer
    assert refresh_obj.scheduled_at == interview_data.scheduled_at
    assert refresh_obj.result == interview_data.result
    