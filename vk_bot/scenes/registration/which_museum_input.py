from vkbottle.bot import Message, BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from states.registration import Registration
from settings import state_dispenser
from actions.registration import submit_registration
from utils import get_state_payload


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_WHICH_MUSEUM)
    async def museum_input_handler(message: Message):
        state_payload = message.state_peer.payload if message.state_peer else {}
        state_payload.update({
            "museum": message.text
        })
        await state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        await submit_registration(message, state_payload)

    @labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadRule({
            "cmd": "skip",
            "state": Registration.REGISTRATION_WHICH_MUSEUM.value
        })
    )
    async def skip_museum_question(event: MessageEvent):
        state_payload = await get_state_payload(
            state_dispenser,
            event.peer_id
        )
        state_payload.update({
            "museum": None
        })
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        await submit_registration(event, state_payload)
