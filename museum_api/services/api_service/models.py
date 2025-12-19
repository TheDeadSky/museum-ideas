from typing import List, Optional
from pydantic import BaseModel


class SendFeedbackAnswerRequest(BaseModel):
    """
    Request model for sending feedback answer to user
    """
    sm_id: str
    answer_text: str
    feedback_text: str


class SendMessageToAllRequest(BaseModel):
    """
    Request model for sending message to all users
    """
    message: str
    tg_ids: List[int]


class NotifyUsersAboutCourseRequest(BaseModel):
    """
    Request model for notifying users about course
    """
    users_with_progress: List[str]
    users_without_progress: List[str]


class ApiResponse(BaseModel):
    """
    Response model from the API
    """
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
