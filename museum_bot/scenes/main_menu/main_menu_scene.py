from aiogram.fsm.scene import Scene, on, After
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from actions.main_menu import default_main_menu
from scenes.main_menu.about_project_scene import AboutProjectScene
from scenes.main_menu.feedback_scene import FeedbackScene
from scenes.get_support.get_support_scene import GetSupportScene
from scenes.share_experience.share_experience_scene import ShareExperienceScene
from services.api_service import get_text_from_db


class MainMenuScene(Scene, state="main-menu"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(message, main_menu_text=main_menu_text)

    @on.callback_query.enter()
    async def on_callback_enter(self, callback: CallbackQuery):
        await callback.answer()

        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(callback.message, main_menu_text=main_menu_text)

    @on.callback_query(F.data == "get_support", after=After.goto(GetSupportScene))
    async def get_support(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete_reply_markup()

    @on.callback_query(F.data == "share_experience", after=After.goto(ShareExperienceScene))
    async def share_experience(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete_reply_markup()

    @on.callback_query(F.data == "feedback", after=After.goto(FeedbackScene))
    async def feedback(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete_reply_markup()

    @on.callback_query(F.data == "about_project", after=After.goto(AboutProjectScene))
    async def about_project(self, callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.delete_reply_markup()
