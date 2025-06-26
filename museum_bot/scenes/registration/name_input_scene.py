from aiogram import F
from aiogram.fsm.scene import After, Scene, on

from aiogram.types import (
    CallbackQuery,
    Message,
)

from menus import CONFIRMATION_MENU
from .is_museum_worker_scene import RegistrationIsMuseumWorkerScene
from services.api_service import get_text_from_db


class RegistrationNameInputScene(Scene, state="registration_name"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        name_question = await get_text_from_db("name_question")

        await message.answer(name_question)

    @on.callback_query.enter(F.data == "registration")
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        await self.on_enter(callback_query.message)

    @on.message()
    async def on_answer(self, message: Message):
        await self.wizard.update_data(name=message.text)
        name_confirmation_message = await get_text_from_db("name_confirmation_message")
        await message.answer(name_confirmation_message.format(message.text), reply_markup=CONFIRMATION_MENU)

    @on.callback_query(F.data == "not_confirm")
    async def not_confirm(self, callback_query: CallbackQuery):
        await self.wizard.update_data(name=None)
        await callback_query.answer("Введите Ваше имя заново.")

    @on.callback_query(F.data == "confirm", after=After.goto(RegistrationIsMuseumWorkerScene))
    async def confirm(self, callback_query: CallbackQuery):
        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()
