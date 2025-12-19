from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from db.models import User, UserCourseProgress
from .models import CourseNotificationSmResponse
from services.tg_bot_api_service.service import TgBotAPIService
from services.vk_bot_api_service.service import VkBotAPIService


async def send_notifications_tg(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
    api_service = TgBotAPIService()
    response = await api_service.notify_users_about_course(
        users_with_progress=users_with_progress_ids,
        users_without_progress=users_without_progress_ids,
    )

    if response.success:
        return CourseNotificationSmResponse(
            success=True,
            message=(
                f"Found {len(users_with_progress_ids)} users with progress and "
                f"{len(users_without_progress_ids)} users without progress"
            ),
            users_with_progress=users_with_progress_ids,
            users_without_progress=users_without_progress_ids
        )
    else:
        return CourseNotificationSmResponse(
            success=False,
            message=response.message,
            users_with_progress=users_with_progress_ids,
            users_without_progress=users_without_progress_ids
        )


async def send_notifications_vk(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
    api_service = VkBotAPIService()
    response = await api_service.notify_users_about_course(
        users_with_progress=users_with_progress_ids,
        users_without_progress=users_without_progress_ids,
    )

    if response.success:
        return CourseNotificationSmResponse(
            success=True,
            message=(
                f"Found {len(users_with_progress_ids)} users with progress and "
                f"{len(users_without_progress_ids)} users without progress"
            ),
            users_with_progress=users_with_progress_ids,
            users_without_progress=users_without_progress_ids
        )
    else:
        return CourseNotificationSmResponse(
            success=False,
            message=response.message,
            users_with_progress=users_with_progress_ids,
            users_without_progress=users_without_progress_ids
        )


async def collect_users_for_notification(db: Session, member=User.telegram_id):
    users_with_progress_query = select(
        member
    ).distinct().join(
        UserCourseProgress, User.id == UserCourseProgress.user_id
    ).where(
        member.isnot(None)
    )

    users_with_progress = db.execute(users_with_progress_query).scalars().all()
    users_with_progress = list(users_with_progress) if users_with_progress is None else []

    users_without_progress_query = select(
        member
    ).where(
        and_(
            member.isnot(None),
            ~User.id.in_(
                users_with_progress
            )
        )
    )

    users_without_progress = db.execute(users_without_progress_query).scalars().all()
    users_without_progress = list(users_without_progress) if users_without_progress is None else []

    return users_with_progress, users_without_progress
