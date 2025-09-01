from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser
from actions.general import make_skip_menu
from utils import get_state_payload


def init(labeler: BotLabeler):
    @labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadRule({
            "cmd": "yes",
            "state": Registration.REGISTRATION_IS_MUSEUM_WORKER.value
        })
    )
    async def yes(event: MessageEvent):
        state_payload = await get_state_payload(state_dispenser, event.peer_id)
        state_payload.update({
            "is_museum_worker": True
        })
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        which_museum_question = await get_text_from_db("which_museum_question")
        await event.send_message(
            which_museum_question,
            keyboard=make_skip_menu(for_state=Registration.REGISTRATION_WHICH_MUSEUM.value)
        )

    @labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadRule({
            "cmd": "no",
            "state": Registration.REGISTRATION_IS_MUSEUM_WORKER.value
        })
    )
    async def no(event: MessageEvent):
        state_payload = await get_state_payload(state_dispenser, event.peer_id)
        state_payload.update({
            "is_museum_worker": False
        })
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_OCCUPATION,
            **state_payload
        )
        sphere_of_activity_question = await get_text_from_db("sphere_of_activity_question")
        await event.send_message(sphere_of_activity_question)
