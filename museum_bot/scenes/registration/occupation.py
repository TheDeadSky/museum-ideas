from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from models.registration import RegistrationData
from scenes.main_menu.main_menu_scene import MainMenuScene
from services.api_service import get_text_from_db, register


class RegistrationOccupationScene(Scene, state="registration_occupation"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        sphere_of_activity_question = await get_text_from_db("sphere_of_activity_question")
        await message.answer(sphere_of_activity_question)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.message(after=After.goto(MainMenuScene))
    async def on_answer(self, message: Message):
        await self.wizard.update_data(occupation=message.text)

        raw_data = {
            **await self.wizard.get_data(),
            "telegram_id": message.from_user.id,
            "tg_username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }

        registration_data = RegistrationData(**raw_data)

        await register(registration_data)
