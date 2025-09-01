from vkbottle.bot import BotLabeler, rules, MessageEvent, Message
from vkbottle_types.events.bot_events import GroupEventType

from actions.general import make_confirmation_menu
from services.api_service import get_text_from_db
from utils import make_one_button_menu
from settings import state_dispenser
from states.share_experience import ShareExperienceStates


experience_enter_labeler = BotLabeler()


@experience_enter_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "share_experience",
    })
)
async def on_enter_share_experience(event: MessageEvent):
    entry_message = await get_text_from_db("share_experience_entry_message")
    await event.edit_message(entry_message)
    ask_text = await get_text_from_db("share_experience_format_ask")
    await event.send_message(
        ask_text,
        keyboard=make_one_button_menu("Отмена", {"cmd": "main_menu"}).get_json()
    )
    await state_dispenser.set(
        event.peer_id,
        ShareExperienceStates.SHARE_EXPERIENCE
    )


@experience_enter_labeler.message(state=ShareExperienceStates.SHARE_EXPERIENCE)
async def handle_experience_input(message: Message):
    state_payload = {
        "experience": message.text
    }
    await state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.CONFIRMATION,
        **state_payload
    )
    thank_message = await get_text_from_db("save_message_confirmation")
    await message.answer(
        thank_message,
        keyboard=make_confirmation_menu(ShareExperienceStates.CONFIRMATION.value)
    )
