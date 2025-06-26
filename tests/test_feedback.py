import pytest
from unittest.mock import AsyncMock, MagicMock
from src.api.v1.routes.feedback import submit_feedback
from src.models.models import InterviewModel, FeedbackModel
from src.schemas.feedback import FeedbackCreate, FeedbackCreateData
from fastapi import HTTPException

# python -m pytest tests/feedback.py

@pytest.mark.asyncio
async def test_submit_feedback_success():
    interview_id = 123
    feedback_input = FeedbackCreate(rating=5, comment="Excellent")

    # Mock interview object (ไม่มี feedback มาก่อน)
    interview = InterviewModel(
        id=interview_id,
        candidate_id="abc",
        interviewer="interviewer_x",
        scheduled_at="2025-07-01T08:00:00",
        result="PASS"
    )
    interview.feedback = None  # No feedback so can submit new feedback

    # Mock db session
    mock_db = AsyncMock()

    # mock db.execute().scalars().first() => return interview
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = interview
    mock_db.execute.return_value = mock_result

    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Mock side effect to simulate setting ID on refresh
    async def refresh_side_effect(obj):
        obj.id = 999
        obj.interview_id = interview_id
    mock_db.refresh.side_effect = refresh_side_effect

    # Actual
    response = await submit_feedback(interview_id=interview_id, feedback_data=feedback_input, db=mock_db)

    assert response["status"] is True
    assert response["message"] == "Feedback submitted successfully"
    assert isinstance(response["data"], FeedbackCreateData)
    assert response["data"].rating == 5
    assert response["data"].comment == "Excellent"

    mock_db.execute.assert_awaited_once()
    mock_db.add.assert_called_once()
    add_obj = mock_db.add.call_args[0][0]
    assert isinstance(add_obj, FeedbackModel)
    assert add_obj.interview_id == interview_id
    assert add_obj.rating == 5
    assert add_obj.comment == "Excellent"

    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()
    refresh_obj = mock_db.refresh.call_args[0][0]
    assert refresh_obj.id == 999
    assert refresh_obj.interview_id == interview_id
    assert refresh_obj.rating == 5
    assert refresh_obj.comment == "Excellent"
    
@pytest.mark.asyncio
async def test_submit_feedback_interview_not_found():
    interview_id = 999
    feedback_input = FeedbackCreate(rating=4, comment="Good")

    mock_db = AsyncMock()

    # จำลองว่า query interview แล้วไม่เจอ
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await submit_feedback(interview_id=interview_id, feedback_data=feedback_input, db=mock_db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Interview not found"

    mock_db.execute.assert_awaited_once()
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_awaited()
    mock_db.refresh.assert_not_awaited()

@pytest.mark.asyncio
async def test_submit_feedback_already_exists():
    # Arrange
    interview_id = 123
    feedback_input = FeedbackCreate(rating=5, comment="Excellent")

    # จำลอง interview ที่มี feedback อยู่แล้ว
    interview_with_feedback = InterviewModel(
        id=interview_id,
        candidate_id="some-candidate-id",
        interviewer="interviewer",
        scheduled_at="2025-07-01T08:00:00",
        result="PASS"
    )
    interview_with_feedback.feedback = FeedbackModel(
        id=1,
        interview_id=interview_id,
        rating=5,
        comment="Already submitted"
    )

    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = interview_with_feedback
    mock_db.execute.return_value = mock_result

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await submit_feedback(interview_id=interview_id, feedback_data=feedback_input, db=mock_db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Feedback already exists"

    mock_db.execute.assert_awaited_once()
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_awaited()
    mock_db.refresh.assert_not_awaited()