from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from aiogram import F

from menus import CANCEL_BUTTON
from scenes.main_menu.main_menu_scene import MainMenuScene
from scenes.share_experience.confirmation_scene import ConfirmationScene
from services.api_service import get_text_from_db


class ShareExperienceScene(Scene, state="share-experience"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        entry_message = await get_text_from_db("share_experience_entry_message")
        await message.edit_text(entry_message)
        ask_text = await get_text_from_db("share_experience_format_ask")
        await message.answer(ask_text, reply_markup=CANCEL_BUTTON)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)

    @on.message(F.text | F.voice | F.audio, after=After.goto(ConfirmationScene))
    async def handle_message(self, message: Message):
        await self.wizard.update_data(experience=message.text or message.voice or message.audio)

    @on.callback_query(F.data == "cancel", after=After.goto(MainMenuScene))
    async def cancel(self, callback: CallbackQuery):
        await callback.answer()
        await callback.message.delete_reply_markup()
