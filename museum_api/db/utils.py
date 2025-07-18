from sqlalchemy.orm import Session
from db.models import User
from typing import Optional


def get_user_by_sm_id(db: Session, sm_id: str) -> Optional[User]:
    """Get user by social media ID (telegram_id or vk_id)"""
    return db.query(User).filter(
        User.telegram_id == sm_id
    ).first()
