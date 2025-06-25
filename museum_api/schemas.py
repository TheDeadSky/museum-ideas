from pydantic import BaseModel, Field, field_validator
from typing import List


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


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

    @field_validator("description", mode="before")
    @classmethod
    def description_validator(cls, v, info):
        if len(v) > 4096:
            raise ValueError("Text of the course must be less than 4096 characters")

        return v

    @field_validator("course_text", mode="before")
    @classmethod
    def course_text_validator(cls, v):
        if len(v) > 4096:
            raise ValueError("Text of the course must be less than 4096 characters")

        return v


class Feedback(BaseModel):
    sm_user_id: str = Field(description="User's social media ID.")
    feedback: str = Field(description="User's feedback.")


class RegistrationData(BaseModel):
    sm_type: str = Field(description="Social media type. `vk` or `tg`")
    telegram_id: str | None = None
    vk_id: str | None = None
    tg_username: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    is_museum_worker: bool = False
    museum: str | None = None
    occupation: str | None = None


class RegistrationResponse(BaseResponse):
    pass


class HistoryData(BaseModel):
    author: str | None = None
    title: str | None = None
    text: str | None = None
    media_url: str | None = None
    link: str | None = None
    is_anonymous: bool = False
    is_agreed_to_publication: bool = True
    content_type: str = Field(default="text", description="`text`, `audio` or `video`")


class HistoryResponse(BaseResponse):
    history: HistoryData
