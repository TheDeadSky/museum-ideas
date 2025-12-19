from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import User
from modules.common.schemas import MessageForAll, MessageForAllResponse
from services.tg_bot_api_service.service import TgBotAPIService
from services.vk_bot_api_service.service import VkBotAPIService
from shared.models import ApiResponse


async def send_message_for_all(message_for_all: MessageForAll, db: Session):
    tg_response = None
    vk_response = None

    if message_for_all.platform in ("tg", "all"):
        tg_response = await send_message_for_all_to_tg(message_for_all, db)

    if message_for_all.platform == ("vk", "all"):
        vk_response = await send_message_for_all_to_vk(message_for_all, db)

    return MessageForAllResponse(
            success=True,
            message="Sending complete",
            platform=message_for_all.platform,
            tg_response=tg_response,
            vk_response=vk_response
        )


async def send_message_for_all_to_tg(message_for_all: MessageForAll, db: Session):
    tg_ids_query = (
        select(
            User.telegram_id
        ).distinct().where(
            User.telegram_id.isnot(None)
        )
    )

    tg_ids = db.execute(tg_ids_query).scalars().all()
    tg_ids = [tg_id for tg_id in tg_ids if tg_id is not None]

    if not tg_ids:
        return ApiResponse(
            success=False,
            message="No users with telegram_id"
        )

    api_service = TgBotAPIService()
    response = await api_service.send_message_to_all(
        message=message_for_all.message,
        tg_ids=tg_ids
    )
    return response


async def send_message_for_all_to_vk(message_for_all: MessageForAll, db: Session):
    vk_ids_query = (
        select(
            User.vk_id
        ).distinct().where(
            User.vk_id.isnot(None)
        )
    )

    vk_ids = db.execute(vk_ids_query).scalars().all()
    vk_ids = [vk_id for vk_id in vk_ids if vk_id is not None]

    if not vk_ids:
        return ApiResponse(
            success=False,
            message="No users with telegram_id"
        )

    api_service = VkBotAPIService()
    response = await api_service.send_message_to_all(
        message=message_for_all.message,
        vk_ids=vk_ids
    )
    return response
