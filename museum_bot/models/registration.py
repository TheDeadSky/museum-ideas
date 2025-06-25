from pydantic import BaseModel, Field


class RegistrationData(BaseModel):
    sm_type: str = Field(default="tg", description="Social media type. `vk` or `tg`")
    telegram_id: str | None = None
    tg_username: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    is_museum_worker: bool = False
    museum: str | None = None
    occupation: str | None = None
