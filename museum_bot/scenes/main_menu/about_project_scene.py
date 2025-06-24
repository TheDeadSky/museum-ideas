from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery

from services.api_service import get_text_from_db
from menus import TO_MAIN_MENU_BUTTON


class AboutProjectScene(Scene, state="about-project"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        about_project_text = await get_text_from_db("about_project_text")
        await message.answer(about_project_text, reply_markup=TO_MAIN_MENU_BUTTON)

    @on.callback_query.enter()
    async def on_callback_enter(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)
