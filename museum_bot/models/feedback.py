from pydantic import BaseModel, Field


class Feedback(BaseModel):
    sm_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")
