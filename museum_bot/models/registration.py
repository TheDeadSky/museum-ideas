from pydantic import BaseModel


class RegistrationData(BaseModel):
    name: str
    telegram_id: str
    is_museum_worker: bool = False
    museum: str | None = None
    occupation: str | None = None
    tg_username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
