import logging

from vkbottle.bot import BotLabeler, Message

from menus import GET_SUPPORT_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import get_text_from_db
from states.general_states import GeneralStates
from utils import merge_inline_menus


get_support_enter_labeler = BotLabeler()


@get_support_enter_labeler.message(
    payload="get_support",
    state=GeneralStates.MAIN_MENU
)
async def on_enter_get_support(message: Message):
    logging.info("Entering GetSupportScene.on_enter")
    entry_message = await get_text_from_db("get_support_entry_message")

    await message.answer(
        entry_message,
        keyboard=merge_inline_menus(
            GET_SUPPORT_MENU,
            TO_MAIN_MENU_BUTTON
        )
    )
