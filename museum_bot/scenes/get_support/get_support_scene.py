import logging

from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from aiogram import F

from menus import GET_SUPPORT_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import get_text_from_db
from utils import merge_inline_menus
from scenes.get_support.self_support_course_scene import SelfSupportCourseScene
from scenes.get_support.show_colleagues_stories import ShowColleaguesStoriesScene


class GetSupportScene(Scene, state="get-support"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        logging.info("Entering GetSupportScene.on_enter")
        entry_message = await get_text_from_db("get_support_entry_message")

        await message.edit_text(
            entry_message,
            reply_markup=merge_inline_menus(
                GET_SUPPORT_MENU,
                TO_MAIN_MENU_BUTTON
            )
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        logging.info("Entering GetSupportScene.on_enter_callback")

        await callback_query.answer()
        await self.on_enter(callback_query.message)

    @on.callback_query(F.data == "self_support", after=After.goto(SelfSupportCourseScene))
    async def on_self_support(self, callback: CallbackQuery):
        logging.info("Self support callback handler: GetSupportScene.on_self_support")
        await callback.answer()
        await callback.message.delete_reply_markup()

    @on.callback_query(F.data == "colleagues_stories", after=After.goto(ShowColleaguesStoriesScene))
    async def on_colleagues_stories(self, callback: CallbackQuery):
        logging.info("Colleagues stories callback handler: GetSupportScene.on_colleagues_stories")
        await callback.answer()
        await callback.message.delete_reply_markup()
