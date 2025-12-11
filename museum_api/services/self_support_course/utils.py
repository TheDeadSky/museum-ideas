import aiohttp
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from db.models import User, UserCourseProgress
from .schemas import CourseNotificationSmResponse


async def send_notifications_tg(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://help-museum_bot:9000/api/notify-users-about-course",
            json={
                "users_with_progress": users_with_progress_ids,
                "users_without_progress": users_without_progress_ids
            }
        ) as response:
            response_data = await response.json()

        if response_data.get("success"):
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
                message=response_data.get("message"),
                users_with_progress = users_with_progress_ids,
                users_without_progress = users_without_progress_ids
            )


async def send_notifications_vk(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://help-vk_bot:9001/api/notify-users-about-course",
            json={
                "users_with_progress": users_with_progress_ids,
                "users_without_progress": users_without_progress_ids
            }
        ) as response:
            response_data = await response.json()

    if response_data.get("success"):
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
            message=response_data.get("message"),
            users_with_progress = users_with_progress_ids,
            users_without_progress = users_without_progress_ids
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
    users_with_progress = list(users_with_progress) if users_with_progress else []

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
    users_without_progress = list(users_without_progress) if users_without_progress else []

    return users_with_progress, users_without_progress
