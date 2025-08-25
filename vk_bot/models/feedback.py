from pydantic import BaseModel, Field


class Feedback(BaseModel):
    sm_type: str = Field(default="vk", description="Social media type")
    vk_id: str
    feedback_text: str
    feedback_type: str = "general" 