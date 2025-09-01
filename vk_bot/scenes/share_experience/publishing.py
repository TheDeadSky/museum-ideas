import logging

from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from actions.general import make_yes_no_menu
from actions.share_experience import submit_share_experience
from states.share_experience import ShareExperienceStates
from settings import state_dispenser
from services.api_service import get_text_from_db
from utils import get_state_payload

experience_publishing_labeler = BotLabeler()


@experience_publishing_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "yes",
        "state": ShareExperienceStates.PUBLISHING.value
    }),
)
async def publish_yes(event: MessageEvent):
    state_payload = await get_state_payload(state_dispenser, event.peer_id)
    state_payload.update({
        "publish": True
    })
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    anonymous_question = await get_text_from_db("anonymous_message_question")
    await event.send_message(
        anonymous_question,
        keyboard=make_yes_no_menu(True, ShareExperienceStates.ANONYMITY.value)
    )


@experience_publishing_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "no",
        "state": ShareExperienceStates.PUBLISHING.value
    })
)
async def publish_no(event: MessageEvent):
    logging.info("publish no")
    state_payload = await get_state_payload(state_dispenser, event.peer_id)
    state_payload.update({
        "publish": False,
        "anonymous": True
    })
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    await submit_share_experience(event, state_payload)
