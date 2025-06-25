from pydantic import BaseModel, Field, field_validator
from typing import List

from utils import escape_tg_reserved_characters


class BotTextRequest(BaseModel):
    keys: List[str]


class SelfSupportCourseBeginnerData(BaseModel):
    user_id: str


class SelfSupportCourse(BaseModel):
    title: str
    description: str
    video_url: str
    course_text: str = Field(description="Text of the course", max_length=4096)
    question: str

    @field_validator("title", mode="before")
    @classmethod
    def title_validator(cls, v, info):
        if len(v) > 255:
            raise ValueError("Text of the course must be less than 255 characters")

        v = escape_tg_reserved_characters(v)

    @field_validator("description", mode="before")
    @classmethod
    def description_validator(cls, v, info):
        if len(v) > 4096:
            raise ValueError("Text of the course must be less than 4096 characters")

        v = escape_tg_reserved_characters(v)

        return v

    @field_validator("course_text", mode="before")
    @classmethod
    def course_text_validator(cls, v):
        if len(v) > 4096:
            raise ValueError("Text of the course must be less than 4096 characters")

        v = escape_tg_reserved_characters(v)

        return v


class Feedback(BaseModel):
    sm_user_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")


class UserRegistration(BaseModel):
    telegram_id: str | None = None
    vk_id: str | None = None
    tg_username: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    is_museum_worker: bool = False
    museum: str | None = None
    occupation: str | None = None


class UserRegistrationResponse(BaseModel):
    success: bool
    message: str
    
