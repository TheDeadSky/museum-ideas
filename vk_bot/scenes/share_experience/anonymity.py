import logging

from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from actions.share_experience import submit_share_experience
from states.share_experience import ShareExperienceStates
from settings import state_dispenser
from utils import get_state_payload


experience_anonymity_labeler = BotLabeler()


@experience_anonymity_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "yes",
        "state": ShareExperienceStates.ANONYMITY.value
    })
)
async def handle_anonymous_yes(event: MessageEvent):
    logging.info("anonymity yes")
    state_payload = await get_state_payload(state_dispenser, event.peer_id)
    state_payload.update({
        "is_anonymous": event.payload == "yes"
    })
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    await submit_share_experience(event, state_payload)


@experience_anonymity_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "no",
        "state": ShareExperienceStates.ANONYMITY.value
    })
)
async def handle_anonymous_no(event: MessageEvent):
    logging.info("anonymity no")
    state_payload = await get_state_payload(state_dispenser, event.peer_id)
    state_payload.update({
        "is_anonymous": event.payload == "yes"
    })
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    await submit_share_experience(event, state_payload)
