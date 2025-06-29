from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery, User

from menus import NEXT_PART_BUTTON, TO_MAIN_MENU_BUTTON
from services.api_service import (
    get_random_achievement_photo_url,
    get_self_support_course_part,
    get_text_from_db,
    self_support_course_answer
)
from utils import merge_inline_menus


class SelfSupportCourseScene(Scene, state="self-support-course"):
    @on.message.enter()
    async def on_enter(self, message: Message, from_user: User):
        self_support_course_response = await get_self_support_course_part(from_user.id)

        if self_support_course_response.success:
            course_data = self_support_course_response.course_data
            part_data = self_support_course_response.part_data

            await self.wizard.update_data(part_id=part_data.id)

            course_title = f"<b>{course_data.title}</b>"
            course_description = f"<i>{course_data.description}</i>"
            await message.answer(f"{course_title}\n{course_description}")

            if part_data.image_url:
                await message.answer_photo(
                    photo=part_data.image_url
                )
            part_title = f"<b>{part_data.title}</b>"
            part_description = f"<i>{part_data.description}</i>"
            await message.answer(f"{part_title}\n{part_description}")

            if part_data.video_url:
                await message.answer(part_data.video_url)

            if part_data.question:
                await message.answer(part_data.question)
            else:
                await self.complete_course_part(message)
        else:
            await message.answer(self_support_course_response.message)
            await message.answer(
                "В ожидании следующей лекции вы можете узнать истории коллег.",
                reply_markup=TO_MAIN_MENU_BUTTON
            )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message, callback_query.from_user)

    @on.message()
    async def on_user_answer(self, message: Message):
        user_answer = message.text

        congratulations_text = await get_text_from_db("congratulations_text")
        achievement_photo = await get_random_achievement_photo_url()

        next_part = await get_self_support_course_part(message.from_user.id)

        markup = TO_MAIN_MENU_BUTTON

        if next_part.success:
            markup = merge_inline_menus(
                NEXT_PART_BUTTON,
                TO_MAIN_MENU_BUTTON,
            )

        await message.answer_photo(
            photo=achievement_photo,
            caption=congratulations_text,
            reply_markup=markup
        )

        await self.complete_course_part(message, user_answer)

    async def complete_course_part(self, message: Message, user_answer: str = None):
        data = await self.wizard.get_data()

        await self_support_course_answer(
            tg_id=str(message.from_user.id),
            part_id=data["part_id"],
            answer=user_answer
        )
