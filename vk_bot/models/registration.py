from pydantic import BaseModel, Field


class RegistrationData(BaseModel):
    sm_type: str = Field(default="vk", description="Social media type. `vk` or `tg`")
    vk_id: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    is_museum_worker: bool = False
    museum: str | None = None
    occupation: str | None = None
