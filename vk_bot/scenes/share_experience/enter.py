from vkbottle.bot import BotLabeler, Message

from menus import CONFIRMATION_MENU
from services.api_service import get_text_from_db
from states.general_states import GeneralStates
from utils import make_one_button_menu
from settings import state_dispenser
from states.share_experience import ShareExperienceStates


experience_enter_labeler = BotLabeler()


@experience_enter_labeler.message(payload="share_experience", state=GeneralStates.MAIN_MENU)
async def on_enter_share_experience(message: Message):
    entry_message = await get_text_from_db("share_experience_entry_message")
    await message.edit_text(entry_message)
    ask_text = await get_text_from_db("share_experience_format_ask")
    await message.answer(ask_text, reply_markup=make_one_button_menu("Отмена", "menu"))
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.SHARE_EXPERIENCE
    )


@experience_enter_labeler.message(state=ShareExperienceStates.SHARE_EXPERIENCE)
async def handle_experience_input(message: Message):
    state_payload = message.state_peer.payload
    state_payload.update({
        "experience": message.text
    })
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.CONFIRMATION,
        **state_payload
    )
    thank_message = await get_text_from_db("save_message_confirmation")
    await message.answer(thank_message, keyboard=CONFIRMATION_MENU)
