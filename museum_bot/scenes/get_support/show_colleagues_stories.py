from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery

from menus import TO_MAIN_MENU_BUTTON, GET_SUPPORT_MENU
from actions.stories import get_random_story
from utils import merge_inline_menus


class ShowColleaguesStoriesScene(Scene, state="colleagues-stories"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        story = await get_random_story()

        if not story:
            await message.edit_text(
                "К сожалению, сейчас нет доступных историй. Попробуйте позже.",
                reply_markup=merge_inline_menus(
                    GET_SUPPORT_MENU,
                    TO_MAIN_MENU_BUTTON
                )
            )
            return

        if story['type'] == "text":
            await message.edit_text(
                story['content'],
                reply_markup=TO_MAIN_MENU_BUTTON
            )

        elif story['type'] == "video":
            await message.edit_text(
                story['content'],
                reply_markup=TO_MAIN_MENU_BUTTON
            )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)
