from aiogram.fsm.scene import Scene, on
from aiogram.types import (
    Message,
    CallbackQuery,
    User
)

from actions.registration import make_registration_button
from models.registration import RegistrationData
from scenes.main_menu.main_menu_scene import MainMenuScene
from services.api_service import register


class SubmitRegistrationScene(Scene, state="submit-registration"):
    @on.message.enter()
    async def on_enter(self, message: Message, from_user: User = None):
        if from_user is None:
            from_user = message.from_user

        raw_data = {
            **await self.wizard.get_data(),
            "telegram_id": str(from_user.id),
            "tg_username": str(from_user.username)
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

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        # await callback_query.answer()
        await self.on_enter(callback_query.message, callback_query.from_user)
