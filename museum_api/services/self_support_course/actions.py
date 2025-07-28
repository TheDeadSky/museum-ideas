from datetime import datetime

import aiohttp
from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from db.models import UserCourseProgress, Course, CoursePart, User
from db.utils import get_user_by_sm_id
from schemas import BaseResponse
from .schemas import (
    CourseUserAnswer,
    SelfSupportCourseData,
    SelfSupportCoursePartData,
    SelfSupportCourseResponse,
    CourseNotificationResponse
)


async def load_self_support_course(sm_id: str, db: Session) -> SelfSupportCourseResponse:
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

        next_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id,
            CoursePart.order_number == finished_course_part.order_number + 1,
        ).first()

    if next_course_part.date_of_publication > datetime.now():
        return BaseResponse(
            success=False,
            message=f"Следующая лекция выйдет {next_course_part.date_of_publication.strftime('%d.%m.%Y')}"
        )

    if not next_course_part:
        raise HTTPException(status_code=404, detail="No course parts found")

    course_data = SelfSupportCourseData(
        id=course.id,
        title=course.course_name,
        description=course.description
    )

    part_data = SelfSupportCoursePartData(
        id=next_course_part.id,
        title=next_course_part.title,
        description=next_course_part.description,
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
        # Get users with course progress
        users_with_progress_query = select(User.telegram_id).distinct().join(
            UserCourseProgress, User.id == UserCourseProgress.user_id
        ).where(User.telegram_id.isnot(None))

        users_with_progress = db.execute(users_with_progress_query).scalars().all()
        users_with_progress_ids = [str(tg_id) for tg_id in users_with_progress if tg_id]

        # Get users without course progress but subscribed to a course
        users_without_progress_query = select(User.telegram_id).where(
            and_(
                User.telegram_id.isnot(None),
                ~User.id.in_(
                    select(UserCourseProgress.user_id).distinct()
                )
            )
        )

        users_without_progress = db.execute(users_without_progress_query).scalars().all()
        users_without_progress_ids = [str(tg_id) for tg_id in users_without_progress if tg_id]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://museum_bot:9000/api/notify-users-about-course",
                json={
                    "users_with_progress": users_with_progress_ids,
                    "users_without_progress": users_without_progress_ids
                }
            ) as response:
                response_data = await response.json()

        if response_data.get("success"):
            return CourseNotificationResponse(
                success=True,
                message=(
                    f"Found {len(users_with_progress_ids)} users with progress and "
                    f"{len(users_without_progress_ids)} users without progress"
                )
            )
        else:
            return CourseNotificationResponse(
                success=False,
                message=response_data.get("message")
            )

    except Exception as e:
        return CourseNotificationResponse(
            success=False,
            message=f"Error getting user notifications: {str(e)}"
        )
