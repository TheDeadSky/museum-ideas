from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None


class CourseNotificationResponse(BaseResponse):
    pass
