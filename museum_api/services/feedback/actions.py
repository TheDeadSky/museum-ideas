from sqlalchemy.orm import Session

from db.utils import get_user_by_sm_id
from db.models import UserQuestion
from schemas import BaseResponse
from .schemas import Feedback


async def save_user_feedback(feedback: Feedback, db: Session):
    user = get_user_by_sm_id(db, feedback.sm_id)

    user_question = UserQuestion(
        user_id=user.id,
        question=feedback.feedback
    )

    db.add(user_question)
    db.commit()
    db.refresh(user_question)

    return BaseResponse(
        success=True,
        message="Спасибо за ваш отзыв!"
    )
