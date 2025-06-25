from pydantic import BaseModel


class RegistrationData(BaseModel):
    name: str
    is_museum_worker: bool
    museum: str | None
    occupation: str | None
    telegram_id: str | None
    tg_username: str | None
    first_name: str | None
    last_name: str | None
