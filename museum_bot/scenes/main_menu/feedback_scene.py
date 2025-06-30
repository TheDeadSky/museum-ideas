import logging
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery
from aiogram import F

from menus import CONFIRMATION_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import send_feedback
from models.feedback import Feedback


class FeedbackScene(Scene, state="feedback"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        await message.edit_text(
            "Введите сообщение для руководителя проекта",
            reply_markup=TO_MAIN_MENU_BUTTON
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.callback_query(F.data == "cancel")
    async def cancel_feedback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text("Отправка отзыва отменена", reply_markup=TO_MAIN_MENU_BUTTON)

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

        await send_feedback(
            Feedback(
                sm_id=callback_query.from_user.id,
                feedback=await self.wizard.get_data()["feedback_text"]
            )
        )

        await callback_query.message.edit_text("Спасибо за ваш отзыв!", reply_markup=TO_MAIN_MENU_BUTTON)

    @on.callback_query(F.data == "not_confirm")
    async def not_confirm_feedback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        await self.on_enter(callback_query.message)
