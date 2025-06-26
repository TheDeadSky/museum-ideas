from pydantic import BaseModel, Field

from schemas import BaseResponse


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
