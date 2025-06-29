from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery
from aiogram import F

from scenes.share_experience.anonymity_scene import AnonymityScene
from services.api_service import get_text_from_db
from menus import YES_NO_MENU


class PublicationScene(Scene, state="share-experience-publication"):
    @on.message.enter()
    async def on_enter(self, message: CallbackQuery):
        publish_question = await get_text_from_db("publish_message_question")
        await message.edit_text(publish_question, reply_markup=YES_NO_MENU)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)

    @on.callback_query(F.data.in_(["yes", "no"]), after=After.goto(AnonymityScene))
    async def publish_yes(self, callback: CallbackQuery):
        await callback.answer()
        await self.wizard.update_data(publish=callback.data == "yes")
