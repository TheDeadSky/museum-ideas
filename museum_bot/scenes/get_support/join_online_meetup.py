from aiogram.fsm.scene import Scene, on
from aiogram.types import Message, CallbackQuery
from aiogram import F

from menus import JOIN_ONLINE_MEETUP_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import get_text_from_db
from utils import merge_inline_menus


class JoinOnlineMeetup(Scene, state="join-online-meetup"):
    @on.message.enter()
    async def on_enter(self, message: Message):
        join_online_meetup_text = await get_text_from_db("join_online_meetup_text")
        await message.answer(
            join_online_meetup_text,
            reply_markup=merge_inline_menus(
                JOIN_ONLINE_MEETUP_MENU,
                TO_MAIN_MENU_BUTTON
            )
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await self.on_enter(callback.message)

    @on.callback_query(F.data == "no")
    async def dont_join_online_meetup(callback: CallbackQuery):
        dont_join_online_meetup_text = await get_text_from_db("dont_join_online_meetup_text")

        await callback.message.edit_text(
            dont_join_online_meetup_text,
            reply_markup=TO_MAIN_MENU_BUTTON
        )
