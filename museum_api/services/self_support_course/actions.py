import logging

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy import or_

from db.models import UserCourseProgress, Course, CoursePart, User
from db.utils import get_user_by_sm_id
from schemas import BaseResponse
from services.self_support_course.utils import send_notifications_tg, send_notifications_vk
from .schemas import (
    CourseUserAnswer,
    SelfSupportCourseData,
    SelfSupportCoursePartData,
    SelfSupportCourseResponse,
    CourseNotificationResponse
)

try:
    from sentry_sdk import capture_exception, capture_message
    sentry_imported = True
except ImportError:
    sentry_imported = False


async def load_self_support_course(sm_id: int, db: Session) -> SelfSupportCourseResponse | BaseResponse:
    user = get_user_by_sm_id(db, sm_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found by sm_id({sm_id})")

    course = db.query(Course).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    user_progress = db.query(UserCourseProgress).filter(
        UserCourseProgress.user_id == user.id
    ).order_by(UserCourseProgress.date.desc()).first()

    if not user_progress:
        next_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id
        ).order_by(CoursePart.order_number).first()

    else:
        finished_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id,
            CoursePart.id == user_progress.part_id
        ).first()

        if finished_course_part:
            finished_course_part_number = finished_course_part.order_number if finished_course_part.order_number else 0
            next_course_part = db.query(CoursePart).filter(
                CoursePart.course_id == course.id,
                CoursePart.order_number == finished_course_part_number + 1,
            ).first()
        else:
            return BaseResponse(
                success=False,
                message=f"Not found finished course part for course(id={course.id}) & part({user_progress.part_id})"
            )

    if next_course_part.date_of_publication > datetime.now():
        return BaseResponse(
            success=False,
            message=f"Следующая лекция выйдет {next_course_part.date_of_publication.strftime('%d.%m.%Y')}"
        )

    if not next_course_part:
        raise HTTPException(status_code=404, detail="No course parts found")

    course_title = course.course_name if course.course_name else ""
    course_description = course.description if course.description else ""
    course_data = SelfSupportCourseData(
        id=course.id,
        title=course_title,
        description=course_description
    )

    part_title = next_course_part.title if next_course_part.title else ""
    part_description = next_course_part.description if next_course_part.description else ""
    part_data = SelfSupportCoursePartData(
        id=next_course_part.id,
        title=part_title,
        description=part_description,
        video_url=next_course_part.video_url,
        image_url=next_course_part.image_url,
        course_text=next_course_part.description,
        question=next_course_part.question,
        publication_date=next_course_part.date_of_publication
    )

    self_support_course_schema = SelfSupportCourseResponse(
        success=True,
        message="Начата новая часть курса",
        course_data=course_data,
        part_data=part_data
    )

    return self_support_course_schema


async def save_self_support_course_answer(answer_data: CourseUserAnswer, db: Session) -> BaseResponse:
    user = get_user_by_sm_id(db, answer_data.sm_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found by sm_id({answer_data.sm_id})")

    user_progress = UserCourseProgress(
        user_id=user.id,
        part_id=answer_data.part_id,
        date=datetime.now(),
        answer=answer_data.answer
    )
    db.add(user_progress)
    db.commit()

    return BaseResponse(
        success=True,
        message="Ответ сохранен"
    )


async def new_course_part_notify(db: Session) -> CourseNotificationResponse:
    try:
        users_with_progress_query = select(
            User.telegram_id,
            User.vk_id
        ).distinct().join(
            UserCourseProgress, User.id == UserCourseProgress.user_id
        ).where(
            or_(
                User.telegram_id.isnot(None),
                User.vk_id.isnot(None)
            )
        )

        users_with_progress = db.execute(users_with_progress_query).scalars().all()
        users_with_progress_tg_ids = []
        users_with_progress_vk_ids = []

        if sentry_imported:
            capture_message("new_course_part_notify", "debug", {
                "users_with_progress": str(users_with_progress)
            })

        for sm_ids in users_with_progress:
            tg_id, vk_id = sm_ids
            if tg_id:
                users_with_progress_tg_ids.append(tg_id)
            if vk_id:
                users_with_progress_vk_ids.append(vk_id)

        users_without_progress_query = select(
            User.telegram_id,
            User.vk_id
        ).where(
            and_(
                or_(
                    User.telegram_id.isnot(None),
                    User.vk_id.isnot(None)
                ),
                ~User.id.in_(
                    select(UserCourseProgress.user_id).distinct()
                )
            )
        )

        users_without_progress = db.execute(users_without_progress_query).scalars().all()
        users_without_progress_tg_ids = []
        users_without_progress_vk_ids = []

        for sm_ids in users_without_progress:
            tg_id, vk_id = sm_ids
            if tg_id:
                users_without_progress_tg_ids.append(tg_id)
            if vk_id:
                users_without_progress_vk_ids.append(vk_id)

        tg_response = await send_notifications_tg(users_with_progress_tg_ids, users_without_progress_tg_ids)

        try:
            vk_response = await send_notifications_vk(users_with_progress_vk_ids, users_without_progress_vk_ids)
        except Exception as e:
            logging.error("", e)
            vk_response = None

        return CourseNotificationResponse(
            success=True,
            message="All messages was send to bots",
            tg_response=tg_response,
            vk_response=vk_response,
        )

    except Exception as e:
        if sentry_imported:
            capture_exception(e)
        return CourseNotificationResponse(
            success=False,
            message=f"Error getting user notifications: {str(e)}",
            tg_response=None,
            vk_response=None,
        )
