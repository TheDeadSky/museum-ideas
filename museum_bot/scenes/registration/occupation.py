from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from scenes.registration.submit_registration import SubmitRegistrationScene
from services.api_service import get_text_from_db


class RegistrationOccupationScene(Scene, state="registration_occupation"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        sphere_of_activity_question = await get_text_from_db("sphere_of_activity_question")
        await message.answer(sphere_of_activity_question)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message(after=After.goto(SubmitRegistrationScene))
    async def on_answer(self, message: Message):
        await self.wizard.update_data(occupation=message.text)
