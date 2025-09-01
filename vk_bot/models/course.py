from datetime import datetime
from pydantic import BaseModel, Field
from models.base import BaseResponse


class SelfSupportCoursePartData(BaseModel):
    id: int
    title: str
    description: str = Field(description="Text of the course", max_length=4096)
    video_url: str | None = None
    image_url: str | None = None
    question: str | None = Field(default=None, description="Question for the user", max_length=4096)
    publication_date: datetime


class SelfSupportCourseData(BaseModel):
    id: int
    title: str
    description: str


class SelfSupportCourseResponse(BaseResponse):
    course_data: SelfSupportCourseData
    part_data: SelfSupportCoursePartData


class CourseUserAnswer(BaseModel):
    answer: str
    part_id: int
    sm_id: str


class CourseNotificationData(BaseModel):
    users_with_progress: list[str] = []
    users_without_progress: list[str] = []
