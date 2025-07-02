from datetime import datetime

from sqlalchemy.orm import Session

from db.utils import get_user_by_sm_id
from db.models import UserQuestion
from schemas import BaseResponse
from .schemas import Feedback, FeedbackAnswerData, FeedbackListResponse, IncomingFeedback


async def save_user_feedback(feedback: IncomingFeedback, db: Session):
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


async def get_feedbacks(page: int, per_page: int, search: str, status: str, db: Session):
    feedbacks = db.query(UserQuestion).filter(
        UserQuestion.question.like(f"%{search}%"),
        UserQuestion.status == status
    ).offset((page - 1) * per_page).limit(per_page).all()

    response = FeedbackListResponse(
        feedbacks=[Feedback(
            id=fb.id,
            user_id=fb.user_id,
            user_name=fb.user.firstname,
            question=fb.question,
            question_date=fb.question_date,
            answer=fb.answer,
            answer_date=fb.answer_date,
            viewed=fb.viewed
        ) for fb in feedbacks]
    )

    return response


async def render_feedbacks_page():
    with open("services/feedback/templates/feedbacks.html", "r") as file:
        html_content = file.read()

    return html_content


async def answer_feedback(answer_data: FeedbackAnswerData, db: Session):
    feedback = db.query(UserQuestion).filter(UserQuestion.id == answer_data.feedback_id).first()

    feedback.answer = answer_data.answer
    feedback.answer_date = datetime.now()

    db.commit()
    db.refresh(feedback)

    return BaseResponse(
        success=True,
        message="Ответ записан"
    )
