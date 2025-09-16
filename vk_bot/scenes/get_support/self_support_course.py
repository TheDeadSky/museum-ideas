from vkbottle.bot import Message, BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from menus import NEXT_PART_BUTTON, TO_MAIN_MENU_BUTTON
from services.api_service import (
    get_random_achievement_photo_url,
    get_self_support_course_part,
    get_text_from_db,
    self_support_course_answer
)
from states.general_states import GeneralStates
from utils import make_one_button_menu, merge_inline_menus, get_state_payload, fetch_binary_data
from settings import state_dispenser, video_uploader, photo_message_uploader


self_support_course_labeler = BotLabeler()


@self_support_course_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "self_support_course"
    })
)
async def on_enter_self_support_course(event: MessageEvent):
    self_support_course_response = await get_self_support_course_part(str(event.peer_id))

    if self_support_course_response.success:
        course_data = self_support_course_response.course_data
        part_data = self_support_course_response.part_data

        state_payload = await get_state_payload(state_dispenser, event.peer_id)
        state_payload.update({"part_id": part_data.id, "is_last_part": part_data.is_last_part})

        await state_dispenser.set(
            event.peer_id,
            GeneralStates.SELF_SUPPORT_COURSE,
            **state_payload
        )

        course_title = course_data.title
        course_description = course_data.description
        await event.send_message(f"{course_title}\n{course_description}")

        if part_data.image_url:
            photo_data = await fetch_binary_data(part_data.image_url)
            photo = await photo_message_uploader.upload(
                file_source=photo_data
            )
            await event.send_message(
                attachment=photo
            )
        part_title = part_data.title
        part_description = part_data.description
        await event.send_message(f"{part_title}\n{part_description}")

        if part_data.vk_video_id:
            await event.send_message("🎥 Видео:")
            await event.send_message(attachment=part_data.vk_video_id)

        await event.send_message(f"❓ {part_data.question}")

    else:
        await event.send_message(self_support_course_response.message)
        await event.send_message(
            "В ожидании следующей лекции вы можете узнать истории коллег.",
            keyboard=merge_inline_menus(
                make_one_button_menu("Узнать истории коллег", {"cmd": "colleagues_stories"}),
                TO_MAIN_MENU_BUTTON
            ).get_json()
        )


@self_support_course_labeler.message(state=GeneralStates.SELF_SUPPORT_COURSE)
async def on_user_answer(message: Message):
    user_answer = message.text
    state_payload = message.state_peer.payload
    is_last_part: bool = state_payload["is_last_part"]

    await self_support_course_answer(
        vk_id=str(message.peer_id),
        part_id=state_payload["part_id"],
        answer=user_answer
    )

    achievement_url = await get_random_achievement_photo_url()
    achievement_binary = await fetch_binary_data(achievement_url)
    achievement_photo = await photo_message_uploader.upload(
        file_source=achievement_binary
    )

    keyboard = TO_MAIN_MENU_BUTTON.get_json()

    if is_last_part:
        last_part_text = get_text_from_db("last_course_part_text")
        await message.answer(
            last_part_text,
            attachment=achievement_photo,
            keyboard=keyboard
        )
    else:
        congratulations_text = await get_text_from_db("congratulations_text")

        next_part = await get_self_support_course_part(str(message.peer_id))

        if next_part.success:
            keyboard = merge_inline_menus(
                NEXT_PART_BUTTON,
                TO_MAIN_MENU_BUTTON,
            ).get_json()

        await message.answer(
            congratulations_text,
            attachment=achievement_photo,
            keyboard=keyboard
        )


@self_support_course_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "self_support_next_part"
    })
)
async def next_part_handler(event: MessageEvent):
    await on_enter_self_support_course(event)
