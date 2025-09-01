import logging

from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from menus import GET_SUPPORT_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import get_text_from_db
from settings import state_dispenser
from states.general_states import GeneralStates
from utils import merge_inline_menus


get_support_enter_labeler = BotLabeler()


@get_support_enter_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "get_support",
    })
)
async def on_enter_get_support(event: MessageEvent):
    logging.info("Entering GetSupportScene.on_enter")
    entry_message = await get_text_from_db("get_support_entry_message")

    await state_dispenser.set(
        event.peer_id,
        GeneralStates.GET_SUPPORT
    )

    await event.send_message(
        entry_message,
        keyboard=merge_inline_menus(
            GET_SUPPORT_MENU,
            TO_MAIN_MENU_BUTTON
        ).get_json()
    )
