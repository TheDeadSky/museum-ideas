from pydantic import BaseModel, Field


class Feedback(BaseModel):
    sm_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")


class FeedbackAnswer(BaseModel):
    sm_id: str = Field(description="Social media user ID to send the response to")
    answer_text: str = Field(description="Response text to send to the user")
    feedback_text: str = Field(description="Original feedback text")
