from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from .schemas import SelfSupportCourseResponse, CourseUserAnswer, CourseNotificationResponse
from .actions import (
    load_self_support_course,
    save_self_support_course_answer,
    new_course_part_notify
)

router = APIRouter()


@router.post("/self-support-course/{sm_id}")
async def get_self_support_course(
    sm_id: str,
    db: Session = Depends(get_db)
) -> SelfSupportCourseResponse:
    """Get a self-support course for a user"""
    self_support_course = await load_self_support_course(sm_id, db)

    return self_support_course


@router.post("/self-support-course/{sm_id}/answer")
async def answer_self_support_course(
    answer_data: CourseUserAnswer,
    db: Session = Depends(get_db)
) -> SelfSupportCourseResponse:
    """Answer a self-support course question"""
    return await save_self_support_course_answer(answer_data, db)


@router.post("/notify-users-about-course")
async def new_course_part_notification_tg(db: Session = Depends(get_db)) -> CourseNotificationResponse:
    """Get users telegram IDs split by course progress status"""

    return await new_course_part_notify(db)
