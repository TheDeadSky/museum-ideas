from vkbottle.bot import BotLabeler, rules, MessageEvent, Message
from vkbottle_types.events.bot_events import GroupEventType

from actions.general import make_yes_no_menu
from scenes.share_experience.enter import on_enter_share_experience
from states.general_states import GeneralStates
from states.share_experience import ShareExperienceStates
from settings import state_dispenser
from services.api_service import get_text_from_db
from utils import get_state_payload

experience_confirmation_labeler = BotLabeler()


@experience_confirmation_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "confirm",
        "state": ShareExperienceStates.CONFIRMATION.value
    })
)
async def confirm(event: MessageEvent):
    state_payload = await get_state_payload(state_dispenser, event.peer_id)
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.PUBLISHING,
        **state_payload
    )
    publish_question = await get_text_from_db("publish_message_question")
    await event.edit_message(
        publish_question,
        keyboard=make_yes_no_menu(for_state=ShareExperienceStates.PUBLISHING.value)
    )


@experience_confirmation_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "not_confirm",
        "state": ShareExperienceStates.CONFIRMATION.value
    })
)
async def not_confirm(message: Message):
    await state_dispenser.set(
        message.peer_id,
        GeneralStates.MAIN_MENU,
        experience=None
    )
    await on_enter_share_experience(message)
