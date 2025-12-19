from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.utils import define_user_platform, get_user_by_sm_id
from db.models import User, UserQuestion
from shared.models import BaseResponse
from services.vk_bot_api_service.service import VkBotAPIService
from .models import Feedback, FeedbackAnswerData, FeedbackListResponse, IncomingFeedback
from services.tg_bot_api_service.service import TgBotAPIService


async def save_user_feedback(feedback: IncomingFeedback, db: Session):
    user = get_user_by_sm_id(db, feedback.sm_id)

    if not user:
        return BaseResponse(
            success=False,
            message=f"User not found by sm_id: {feedback.sm_id}"
        )

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


async def get_feedbacks(
    db: Session,
    page: int = 1,
    per_page: int = 10,
    search: str = "",
    status: str = ""
):
    filters = []

    if status:
        if status == "answered":
            filters.append(UserQuestion.answer.isnot(None))
        elif status == "pending":
            filters.append(UserQuestion.answer.is_(None))

    if search:
        filters.append(UserQuestion.question.like(f"%{search}%"))

    feedbacks = db.query(UserQuestion).filter(
        and_(*filters)
    ).offset((page - 1) * per_page).limit(per_page).all()

    response = FeedbackListResponse(
        success=True,
        message="Отзывы получены",
        feedbacks=[Feedback(
            id=fb.id,
            user_id=fb.user_id,  # type: ignore
            user_name=fb.user.firstname,  # type: ignore
            question=fb.question,  # type: ignore
            question_date=fb.question_date,  # type: ignore
            answer=fb.answer,
            answer_date=fb.answer_date,  # type: ignore
            viewed=fb.viewed  # type: ignore
        ) for fb in feedbacks]
    )

    return response


async def render_feedbacks_page():
    with open("services/feedback/templates/feedbacks.html", "r") as file:
        html_content = file.read()

    return html_content


async def answer_feedback(answer_data: FeedbackAnswerData, db: Session):
    feedback = db.query(UserQuestion).filter(UserQuestion.id == answer_data.feedback_id).first()

    if not feedback:
        return BaseResponse(
            success=False,
            message=f"Feedback(id={answer_data.feedback_id}) not found"
        )

    feedback.answer = answer_data.answer
    feedback.answer_date = datetime.now()  # type: ignore

    db.commit()
    db.refresh(feedback)

    response = await send_answer_to_user(answer_data, db)
    print(response)

    return BaseResponse(
        success=True,
        message="Ответ записан"
    )


async def send_answer_to_user(feedback_answer: FeedbackAnswerData, db: Session):
    print("feedback_answer", feedback_answer)

    user = db.query(User).filter(User.id == feedback_answer.user_id).first()

    if not user:
        return BaseResponse(
            success=False,
            message="Пользователь не найден"
        )

    feedback = db.query(UserQuestion).filter(UserQuestion.id == feedback_answer.feedback_id).first()

    if not feedback:
        return BaseResponse(
            success=False,
            message="Обратная связь не найдена"
        )

    print(
        "send_answer_to_user",
        {
            "sm_id": user.telegram_id,
            "answer_text": feedback_answer.answer,
            "feedback_text": feedback.question
        }
    )

    platform = define_user_platform(db, user)

    if platform == "tg":
        api_service = TgBotAPIService()
        sm_id = user.telegram_id
    elif platform == "vk":
        api_service = VkBotAPIService()
        sm_id = user.vk_id
    else:
        raise ValueError(f"Unknown platform: '{platform}'")

    if not sm_id:
        raise ValueError(
            f"User({user.id}|{user.firstname} {user.lastname}) has no any social media id."
        )

    response = await api_service.send_feedback_answer(
        sm_id=sm_id,
        answer_text=feedback_answer.answer,
        feedback_text=feedback.question or ""
    )
    return response
