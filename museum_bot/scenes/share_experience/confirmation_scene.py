from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from aiogram import F

from scenes.share_experience.publication_scene import PublicationScene
from services.api_service import get_text_from_db
from menus import CONFIRMATION_MENU


class ConfirmationScene(Scene, state="share-experience-confirmation"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        thank_message = await get_text_from_db("save_message_confirmation")
        await message.answer(thank_message, reply_markup=CONFIRMATION_MENU)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)

    @on.callback_query(F.data == "confirm", after=After.goto(PublicationScene))
    async def confirm_message(self, callback: CallbackQuery):
        await callback.answer()

    @on.callback_query(F.data == "not_confirm", after=After.back())
    async def not_confirm_message(self, callback: CallbackQuery):
        await callback.answer()
