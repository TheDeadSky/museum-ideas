import logging
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery
from aiogram import F

from menus import CONFIRMATION_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import send_feedback, get_text_from_db
from models.feedback import Feedback
from utils import make_one_button_menu


class FeedbackScene(Scene, state="feedback"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        feedback_entry_message = await get_text_from_db("feedback_entry_message")

        await message.edit_text(
            feedback_entry_message,
            reply_markup=make_one_button_menu("Отмена", "menu")
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message()
    async def handle_feedback(self, message: Message):
        await self.wizard.update_data(feedback_text=message.text)
        await message.answer(
            "Подтвердите отправку отзыва:",
            reply_markup=CONFIRMATION_MENU
        )

    @on.callback_query(F.data == "confirm")
    async def confirm_feedback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        logging.info(
            str(await self.wizard.get_data())
        )

        data = await self.wizard.get_data()

        await send_feedback(
            Feedback(
                sm_id=str(callback_query.from_user.id),
                feedback=data["feedback_text"]
            )
        )

        feedback_accepted_message = await get_text_from_db("feedback_accepted_message")

        await callback_query.message.edit_text(feedback_accepted_message, reply_markup=TO_MAIN_MENU_BUTTON)

    @on.callback_query(F.data == "not_confirm")
    async def not_confirm_feedback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        await self.on_enter(callback_query.message)
