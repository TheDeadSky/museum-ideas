from pydantic import BaseModel, Field
from typing import List


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


class BotTextRequest(BaseModel):
    keys: List[str]


class Feedback(BaseModel):
    sm_user_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")
