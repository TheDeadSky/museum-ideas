from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery
from aiogram import F

from services.api_service import get_text_from_db
from menus import TO_MAIN_MENU_BUTTON, YES_NO_MENU


class AnonymityScene(Scene, state="share-experience-anonymity"):
    @on.message.enter()
    async def on_enter(self, message: CallbackQuery):
        anonymous_question = await get_text_from_db("anonymous_message_question")
        await message.edit_text(anonymous_question, reply_markup=YES_NO_MENU)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)

    @on.callback_query(F.data.in_(["yes", "no"]))
    async def handle_anonymous(self, callback: CallbackQuery):
        await callback.answer()
        is_anonymous = callback.data == "yes"
        await self.wizard.update_data(anonymous=is_anonymous)

        data = await self.wizard.get_data()
        final_message = await get_text_from_db("final_thank_message")
        await callback.message.edit_text(
            f"{final_message}\n\n"
            f"Ваше сообщение:  {data['user_message']}\n"
            f"Публикация: {'Да' if data.get('publish') else 'Нет'}\n"
            f"Анонимно: {'Да' if is_anonymous else 'Нет'}",
            reply_markup=TO_MAIN_MENU_BUTTON
        )
