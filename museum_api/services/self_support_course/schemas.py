from datetime import datetime

from pydantic import BaseModel, Field

from schemas import BaseResponse


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
    publication_date: datetime | None


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


class CourseNotificationSmResponse(BaseResponse):
    users_with_progress: list[str]
    users_without_progress: list[str]


class CourseNotificationResponse(BaseResponse):
    tg_response: CourseNotificationSmResponse | None = None
    vk_response: CourseNotificationSmResponse | None = None
