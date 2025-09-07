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
from utils import make_one_button_menu, merge_inline_menus, get_state_payload
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
        state_payload.update({"part_id": part_data.id})

        await state_dispenser.set(
            event.peer_id,
            GeneralStates.SELF_SUPPORT_COURSE,
            **state_payload
        )

        course_title = course_data.title
        course_description = course_data.description
        await event.send_message(f"{course_title}\n{course_description}")

        if part_data.image_url:
            photo = await photo_message_uploader.upload(
                file_source=part_data.image_url
            )
            await event.send_message(
                attachment=photo
            )
        part_title = part_data.title
        part_description = part_data.description
        await event.send_message(f"{part_title}\n{part_description}")

        if part_data.video_url:
            video = await video_uploader.upload(
                link=part_data.video_url,
                peer_id=event.peer_id,
            )
            await event.send_message("🎥 Видео:")
            await event.send_message(attachment=video)

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

    congratulations_text = await get_text_from_db("congratulations_text")
    achievement_photo = await get_random_achievement_photo_url()

    next_part = await get_self_support_course_part(str(message.peer_id))

    keyboard = TO_MAIN_MENU_BUTTON.get_json()

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

    data = message.state_peer.payload if message.state_peer else {}

    await self_support_course_answer(
        vk_id=str(message.peer_id),
        part_id=data["part_id"],
        answer=user_answer
    )


@self_support_course_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "self_support_next_part"
    })
)
async def next_part(event: MessageEvent):
    await on_enter_self_support_course(event)
