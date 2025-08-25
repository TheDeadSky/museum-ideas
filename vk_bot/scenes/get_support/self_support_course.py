from vkbottle.bot import BotLabeler, Message

from menus import NEXT_PART_BUTTON, TO_MAIN_MENU_BUTTON
from services.api_service import (
    get_random_achievement_photo_url,
    get_self_support_course_part,
    get_text_from_db,
    self_support_course_answer
)
from states.general_states import GeneralStates
from utils import make_one_button_menu, merge_inline_menus
from settings import state_dispenser


self_support_course_labeler = BotLabeler()


@self_support_course_labeler.message(payload="self_support_course", state=GeneralStates.GET_SUPPORT)
async def on_enter_self_support_course(message: Message, from_user: User):
    self_support_course_response = await get_self_support_course_part(from_user.id)

    if self_support_course_response.success:
        course_data = self_support_course_response.course_data
        part_data = self_support_course_response.part_data

        state_payload = message.state_peer.payload
        state_payload.update({"part_id": part_data.id})
        state_dispenser.set(
            message.peer_id,
            GeneralStates.SELF_SUPPORT_COURSE,
            **state_payload
        )

        course_title = course_data.title
        course_description = course_data.description
        await message.answer(f"{course_title}\n{course_description}")

        # if part_data.image_url:
        #     await message.answer_photo(
        #         photo=part_data.image_url
        #     )
        part_title = part_data.title
        part_description = part_data.description
        await message.answer(f"{part_title}\n{part_description}")

        # if part_data.video_url:
        #     await message.answer("🎥 Видео:")
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(part_data.video_url) as response:
        #             video_data = await response.read()

        #     file = BufferedInputFile(video_data, "video.mp4")
        #     await message.answer_video(file)

        await message.answer(f"❓ {part_data.question}")

    else:
        await message.answer(self_support_course_response.message)
        await message.answer(
            "В ожидании следующей лекции вы можете узнать истории коллег.",
            keyboard=merge_inline_menus(
                make_one_button_menu("Узнать истории коллег", "colleagues_stories"),
                TO_MAIN_MENU_BUTTON
            )
        )


@self_support_course_labeler.message(state=GeneralStates.SELF_SUPPORT_COURSE)
async def on_user_answer(message: Message):
    user_answer = message.text

    congratulations_text = await get_text_from_db("congratulations_text")
    achievement_photo = await get_random_achievement_photo_url()

    next_part = await get_self_support_course_part(message.peer_id)

    keyboard = TO_MAIN_MENU_BUTTON

    if next_part.success:
        keyboard = merge_inline_menus(
            NEXT_PART_BUTTON,
            TO_MAIN_MENU_BUTTON,
        )

    await message.answer_photo(
        photo=achievement_photo,
        caption=congratulations_text,
        keyboard=keyboard
    )

    data = message.state_peer.payload

    await self_support_course_answer(
        vk_id=str(message.from_user.id),
        part_id=data["part_id"],
        answer=user_answer
    )


@self_support_course_labeler.message(payload="self_support_next_part", state=GeneralStates.SELF_SUPPORT_COURSE)
async def next_part(message: Message):
    await on_enter_self_support_course(message, message.from_user)
