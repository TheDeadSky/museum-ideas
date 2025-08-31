from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser


def init(labeler: BotLabeler):
    # @labeler.raw_event(
    #     GroupEventType.MESSAGE_EVENT,
    #     MessageEvent,
    #     rules.PayloadRule({"cmd": "registration"}),
    #     state=Registration.REGISTRATION_START
    # )
    @labeler.private_message(
        payload={"cmd": "registration"},
        state=Registration.REGISTRATION_START
    )
    async def start_registration(event: MessageEvent):
        name_question = await get_text_from_db("name_question")
        state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_NAME
        )
        await event.send_message(name_question)
