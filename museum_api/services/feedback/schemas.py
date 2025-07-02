from datetime import datetime

from pydantic import BaseModel, Field

from schemas import BaseResponse


class IncomingFeedback(BaseModel):
    sm_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")


class Feedback(BaseModel):
    id: int = Field(description="Feedback ID.")
    user_id: int = Field(description="User ID.")
    user_name: str | None = Field(description="User's name.")
    question: str = Field(description="User's feedback.")
    question_date: datetime = Field(description="Date of feedback.")
    answer: str | None = Field(description="Answer to the feedback.")
    answer_date: datetime | None = Field(description="Date of answer.")
    viewed: datetime | None = Field(description="Date of viewing.")


class FeedbackListResponse(BaseResponse):
    feedbacks: list[Feedback] = Field(description="List of feedbacks.")


class FeedbackAnswerData(BaseModel):
    feedback_id: int = Field(description="Feedback ID.")
    user_id: int = Field(description="User ID.")
    answer: str = Field(description="Answer to the feedback.")
