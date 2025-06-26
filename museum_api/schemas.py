from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


class BotTextRequest(BaseModel):
    keys: List[str]


class SelfSupportCourseBeginnerData(BaseModel):
    user_id: str


class SelfSupportCoursePartData(BaseModel):
    id: int
    title: str
    description: str
    video_url: str | None = None
    image_url: str | None = None
    course_text: str | None = Field(default=None, description="Text of the course", max_length=4096)
    question: str | None = Field(default=None, description="Question for the user", max_length=4096)
    publication_date: datetime


class SelfSupportCourseData(BaseModel):
    id: int
    title: str
    description: str


class SelfSupportCourseResponse(BaseResponse):
    course_data: SelfSupportCourseData | None = None
    part_data: SelfSupportCoursePartData | None = None


class CourseUserAnswer(BaseModel):
    answer: str | None = None
    part_id: int
    sm_id: int


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
