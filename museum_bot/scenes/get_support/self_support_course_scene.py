from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery

from menus import TO_MAIN_MENU_BUTTON
from services.api_service import get_achievement_photo_url, get_self_support_course, get_text_from_db
from aiogram.types import FSInputFile


class SelfSupportCourseScene(Scene, state="self-support-course"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        entry_message = await get_text_from_db("self_support_course_entry_message")

        await message.edit_text(entry_message)

        self_support_course = await get_self_support_course()

        await message.answer(
            self_support_course["video_url"]
        )

        photo = FSInputFile(self_support_course["course_photo_url"])

        # await message.answer(self_support_course["course_text"])
        await message.answer_photo(photo, self_support_course["course_text"])

        await message.answer(
            self_support_course["question"],
            reply_markup=TO_MAIN_MENU_BUTTON
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message()
    async def on_user_answer(self, message: Message):
        user_answer = message.text  # send to API
        print(user_answer)

        congratulations_text = await get_text_from_db("congratulations_text")
        achievement_photo = await get_achievement_photo_url()  # TODO: get this from API

        await message.answer_photo(achievement_photo, congratulations_text)
