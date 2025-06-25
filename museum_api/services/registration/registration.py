from sqlalchemy.orm import Session

from db.models import User
from schemas import RegistrationData, RegistrationResponse
from services.registration.utils import raise_if_user_exist
from .exceptions import RegistrationException


async def registration(registration_data: RegistrationData, db: Session) -> RegistrationResponse:
    raise_if_user_exist(db, registration_data)

    new_user = User(
        telegram_id=registration_data.telegram_id,
        vk_id=registration_data.vk_id,
        tg_username=registration_data.tg_username,
        firstname=registration_data.firstname,
        lastname=registration_data.lastname,
        is_museum_worker=registration_data.is_museum_worker,
        museum=registration_data.museum,
        occupation=registration_data.occupation
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RegistrationResponse(
            success=True,
            message="Регистрация прошла успешно"
        )
    except Exception as e:
        db.rollback()
        raise RegistrationException(f"Failed to register user: {e}")
