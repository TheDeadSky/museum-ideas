from aiogram import F
from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery

from menus import TO_MAIN_MENU_BUTTON, ONE_MORE_STORY_BUTTON
from utils import merge_inline_menus
from services.api_service import get_random_history


class ShowColleaguesStoriesScene(Scene, state="colleagues-stories"):
    @on.message.enter()
    async def on_enter(self, message: Message, tg_user_id: int):
        history_response = await get_random_history(
            str(tg_user_id)
        )

        if not history_response.success:
            await message.answer(
                text=history_response.message,
                reply_markup=TO_MAIN_MENU_BUTTON
            )
            return

        story = history_response.history

        display_text = ""

        if story.title:
            display_text += f"<b>{story.title}</b>\n"

        if story.text:
            if display_text:
                display_text += "\n"
            display_text += story.text

        if story.author and not story.is_anonymous:
            display_text += f"\n\n<i>{story.author}</i>"

        if story.content_type == "text":
            await message.answer(
                display_text,
                reply_markup=merge_inline_menus(
                    ONE_MORE_STORY_BUTTON,
                    TO_MAIN_MENU_BUTTON
                )
            )

        elif story.content_type == "audio":
            await message.answer(
                display_text
            )
            await message.answer_audio(
                story.media_url,
                reply_markup=merge_inline_menus(
                    ONE_MORE_STORY_BUTTON,
                    TO_MAIN_MENU_BUTTON
                )
            )

        elif story.content_type == "video":
            await message.answer(
                display_text
            )
            await message.answer_video(
                story.media_url,
                reply_markup=merge_inline_menus(
                    ONE_MORE_STORY_BUTTON,
                    TO_MAIN_MENU_BUTTON
                )
            )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message, callback_query.from_user.id)

    @on.callback_query(F.data == "one_more_story")
    async def on_one_more_story(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.delete_reply_markup()
        await self.on_enter(callback_query.message, callback_query.from_user.id)
