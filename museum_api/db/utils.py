from sqlalchemy.orm import Session
from db.models import User
from typing import Optional
from sqlalchemy import or_


def get_user_by_sm_id(db: Session, sm_id: str) -> Optional[User]:
    """Get user by social media ID (telegram_id or vk_id)"""
    return db.query(User).filter(
        or_(
            User.telegram_id == sm_id,
            User.vk_id == sm_id
        )
    ).first()


def define_user_platform(db: Session, user: User):
    if user.telegram_id:
        return "tg"
    elif user.vk_id:
        return "vk"
    else:
        raise ValueError(f"User({user.id}|{user.firstname} {user.lastname}) has no any social media id.")
