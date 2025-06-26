from sqlalchemy.orm import Session

from db.models import User
from db.utils import get_user_by_sm_id
from schemas import RegistrationData, RegistrationResponse
from .utils import raise_if_user_exist
from .exceptions import RegistrationException, UserExistException


async def registration(registration_data: RegistrationData, db: Session) -> RegistrationResponse:
    try:
        raise_if_user_exist(registration_data, db)
    except UserExistException:
        return RegistrationResponse(
            success=False,
            message="Пользователь с таким ID уже зарегистрирован.",
        )

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


async def is_user_registered(sm_id: str, db: Session) -> RegistrationResponse:
    user = get_user_by_sm_id(db, sm_id)

    print(user)

    if user:
        return RegistrationResponse(
            success=True,
            message="Пользователь найден"
        )

    return RegistrationResponse(
        success=False,
        message=f"Пользователь не найден. sm_id: {sm_id}"
    )
