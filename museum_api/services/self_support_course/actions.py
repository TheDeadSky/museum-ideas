from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import UserCourseProgress, Course, CoursePart
from db.utils import get_user_by_sm_id
from schemas import BaseResponse
from .schemas import CourseUserAnswer, SelfSupportCourseData, SelfSupportCoursePartData, SelfSupportCourseResponse


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
        answer=answer_data.answer
    )
    db.add(user_progress)
    db.commit()

    return BaseResponse(
        success=True,
        message="Ответ сохранен"
    )
