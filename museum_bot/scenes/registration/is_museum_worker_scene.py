from aiogram import F
from aiogram.fsm.scene import After, Scene, on

from aiogram.types import (
    CallbackQuery,
    Message,
)

from menus import YES_NO_MENU
from .occupation import RegistrationOccupationScene
from .which_museum_scene import RegistrationWhichMuseumScene
from services.api_service import get_text_from_db


class RegistrationIsMuseumWorkerScene(Scene, state="registration_is_museum_worker"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        is_museum_worker_question = await get_text_from_db("is_museum_worker_question")
        await message.answer(is_museum_worker_question, reply_markup=YES_NO_MENU)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.callback_query(F.data == "yes", after=After.goto(RegistrationWhichMuseumScene))
    async def yes_answer(self, callback_query: CallbackQuery):
        await self.wizard.update_data(is_museum_worker=True)
        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()

    @on.callback_query(F.data == "no", after=After.goto(RegistrationOccupationScene))
    async def no_answer(self, callback_query: CallbackQuery):
        await self.wizard.update_data(is_museum_worker=False)
        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()
