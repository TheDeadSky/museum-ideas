from aiogram import F
from aiogram.fsm.scene import After, Scene, on

from aiogram.types import (
    CallbackQuery,
    Message,
)
from menus import SKIP_BUTTON
from scenes.registration.submit_registration import SubmitRegistrationScene
from services.api_service import get_text_from_db


class RegistrationWhichMuseumScene(Scene, state="registration_which_museum"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        which_museum_question = await get_text_from_db("which_museum_question")
        await message.answer(which_museum_question, reply_markup=SKIP_BUTTON)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message(after=After.goto(SubmitRegistrationScene))
    async def which_museum_input(self, message: Message):
        await self.wizard.update_data(museum=message.text)

    @on.callback_query(F.data == "skip", after=After.goto(SubmitRegistrationScene))
    async def skip_museum(self, callback_query: CallbackQuery):
        await self.wizard.update_data(museum=None)
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
