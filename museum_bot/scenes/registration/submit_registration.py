from aiogram.fsm.scene import Scene, on
from aiogram.types import (
    Message
)

from actions.registration import make_registration_button
from models.registration import RegistrationData
from scenes.main_menu.main_menu_scene import MainMenuScene
from services.api_service import register


class SubmitRegistrationScene(Scene, state="submit-registration"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        raw_data = {
            **await self.wizard.get_data(),
            "telegram_id": str(message.from_user.id),
            "tg_username": str(message.from_user.username),
            "first_name": str(message.from_user.first_name),
            "last_name": str(message.from_user.last_name)
        }

        registration_data = RegistrationData(**raw_data)

        result = await register(registration_data)

        if result["success"]:
            await self.wizard.goto(MainMenuScene)
        else:
            registration_button = make_registration_button("Попробовать снова")
            await message.answer(
                "Не удалось зарегистрироваться.",
                reply_markup=registration_button
            )
