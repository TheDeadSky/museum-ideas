from sqlalchemy.orm import Session

from db.models import User
from .schemas import RegistrationData
from .exceptions import RegistrationException, UserExistException


def raise_if_user_exist(registration_data: RegistrationData, db: Session) -> None:
    sm_id: str

    if registration_data.sm_type == "tg":
        sm_id = registration_data.telegram_id
        existing_user = get_user_by_tg_id(db, registration_data.telegram_id)
    elif registration_data.sm_type == "vk":
        sm_id = registration_data.vk_id
        existing_user = get_user_by_vk_id(db, registration_data.vk_id)
    else:
        raise RegistrationException(f"Unknown social media type: {registration_data.sm_type}")

    if existing_user:
        raise UserExistException(f"User with this social media ID({sm_id}) already exists")


def get_user_by_tg_id(db: Session, telegram_id: str):
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def get_user_by_vk_id(db: Session, vk_id: str):
    return db.query(User).filter(User.vk_id == vk_id).first()
