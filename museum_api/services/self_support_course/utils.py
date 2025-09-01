import aiohttp

from .schemas import CourseNotificationSmResponse


async def send_notifications_tg(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
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
            return CourseNotificationSmResponse(
                success=True,
                message=(
                    f"Found {len(users_with_progress_ids)} users with progress and "
                    f"{len(users_without_progress_ids)} users without progress"
                )
            )
        else:
            return CourseNotificationSmResponse(
                success=False,
                message=response_data.get("message")
            )


async def send_notifications_vk(users_with_progress_ids: list[str], users_without_progress_ids: list[str]):
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
        return CourseNotificationSmResponse(
            success=True,
            message=(
                f"Found {len(users_with_progress_ids)} users with progress and "
                f"{len(users_without_progress_ids)} users without progress"
            )
        )
    else:
        return CourseNotificationSmResponse(
            success=False,
            message=response_data.get("message")
        )
