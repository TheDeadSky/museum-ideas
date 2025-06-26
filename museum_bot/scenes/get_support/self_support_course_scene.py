from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery

from scenes.main_menu import MainMenuScene
from services.api_service import (
    get_random_achievement_photo_url,
    get_self_support_course_part,
    get_text_from_db,
    self_support_course_answer
)


class SelfSupportCourseScene(Scene, state="self-support-course"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        self_support_course_response = await get_self_support_course_part(message.from_user.id)

        if self_support_course_response.success:
            course_data = self_support_course_response.course_data
            part_data = self_support_course_response.part_data

            await self.wizard.update_data(part_id=part_data.id)

            if part_data.image_url:
                await message.answer_photo(
                    photo=part_data.image_url
                )
            title = f"<b>{course_data.title}</b>"
            description = f"<i>{course_data.description}</i>"
            await message.answer(f"{title}\n{description}")

            if part_data.video_url:
                await message.answer(part_data.video_url)

            if part_data.question:
                await message.answer(part_data.question)
            else:
                await self.complete_course_part(message)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message()
    async def on_user_answer(self, message: Message):
        user_answer = message.text

        congratulations_text = await get_text_from_db("congratulations_text")
        achievement_photo = await get_random_achievement_photo_url()

        await message.answer_photo(achievement_photo, congratulations_text)
        await self.complete_course_part(message, user_answer)

    async def complete_course_part(self, message: Message, user_answer: str = None):
        await self_support_course_answer(
            tg_id=str(message.from_user.id),
            part_id=await self.wizard.get("part_id"),
            answer=user_answer
        )

        await self.wizard.goto(MainMenuScene)
