from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from scenes.main_menu.main_menu_scene import MainMenuScene
from services.api_service import get_text_from_db


class RegistrationSphereOfActivityScene(Scene, state="registration_sphere_of_activity"):
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
        await self.wizard.update_data(sphere_of_activity=message.text)
        print(await self.wizard.get_data())
