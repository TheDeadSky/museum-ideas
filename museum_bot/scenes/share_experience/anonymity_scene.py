from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery
from aiogram import F

from services.api_service import get_text_from_db
from menus import YES_NO_MENU_SWAPPED_ICONS
from scenes.share_experience.submit_share_experience import SubmitShareExperienceScene


class AnonymityScene(Scene, state="share-experience-anonymity"):
    @on.message.enter()
    async def on_enter(self, message: CallbackQuery):
        anonymous_question = await get_text_from_db("anonymous_message_question")
        await message.edit_text(anonymous_question, reply_markup=YES_NO_MENU_SWAPPED_ICONS)

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)

    @on.callback_query(F.data.in_(["yes", "no"]), after=After.goto(SubmitShareExperienceScene))
    async def handle_anonymous(self, callback: CallbackQuery):
        await callback.answer()
        await callback.message.delete_reply_markup()
        is_anonymous = callback.data == "yes"
        await self.wizard.update_data(is_anonymous=is_anonymous)
