from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from services.api_service import get_text_from_db
from menus import CONFIRMATION_MENU, YES_NO_MENU, TO_MAIN_MENU_BUTTON


class ShareExperienceScene(Scene, state="share-experience"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        entry_message = await get_text_from_db("share_experience_entry_message")
        await message.edit_text(entry_message)

    @on.message(F.text | F.voice | F.audio)
    async def handle_message(self, message: Message, state: FSMContext):
        await state.update_data(user_message=message.text or message.voice or message.audio)
        thank_message = await get_text_from_db("thank_for_message")
        await message.answer(thank_message, reply_markup=CONFIRMATION_MENU)

    @on.callback_query(F.data == "confirm")
    async def confirm_message(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        publish_question = await get_text_from_db("publish_question")
        await callback.message.edit_text(publish_question, reply_markup=YES_NO_MENU)

    @on.callback_query(F.data == "not_confirm")
    async def not_confirm_message(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.edit_text("Сообщение отменено", reply_markup=TO_MAIN_MENU_BUTTON)

    @on.callback_query(F.data == "yes")
    async def publish_yes(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await self.wizard.update_data(publish=True)
        anonymous_question = await get_text_from_db("anonymous_question")
        await callback.message.edit_text(anonymous_question, reply_markup=YES_NO_MENU)

    @on.callback_query(F.data == "no")
    async def publish_no(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await self.wizard.update_data(publish=False)
        anonymous_question = await get_text_from_db("anonymous_question")
        await callback.message.edit_text(anonymous_question, reply_markup=YES_NO_MENU)

    @on.callback_query(F.data.in_(["yes", "no"]), After(lambda c: c.data == "yes" or c.data == "no"))
    async def handle_anonymous(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        is_anonymous = callback.data == "yes"
        await self.wizard.update_data(anonymous=is_anonymous)

        data = await self.wizard.get_data()
        final_message = await get_text_from_db("final_thank_message")
        await callback.message.edit_text(
            f"{final_message}\n\n"
            f"Ваше сообщение: {data['user_message']}\n"
            f"Публикация: {'Да' if data.get('publish') else 'Нет'}\n"
            f"Анонимно: {'Да' if is_anonymous else 'Нет'}",
            reply_markup=TO_MAIN_MENU_BUTTON
        )
