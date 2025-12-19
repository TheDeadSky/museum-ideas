from typing import List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


class SendMessageToAllRequest(BaseModel):
    """
    Request model for sending message to all users
    """
    message: str
    sm_ids: List[str]
