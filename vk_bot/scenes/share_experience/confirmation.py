from vkbottle.bot import BotLabeler, Message

from scenes.share_experience.enter import on_enter_share_experience
from states.general_states import GeneralStates
from states.share_experience import ShareExperienceStates
from settings import state_dispenser
from menus import YES_NO_MENU
from services.api_service import get_text_from_db


experience_confirmation_labeler = BotLabeler()


@experience_confirmation_labeler.message(payload="confirm", state=ShareExperienceStates.CONFIRMATION)
async def confirm(message: Message):
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.PUBLISHING
    )
    publish_question = await get_text_from_db("publish_message_question")
    await message.edit_text(publish_question, reply_markup=YES_NO_MENU)


@experience_confirmation_labeler.message(payload="not_confirm", state=ShareExperienceStates.CONFIRMATION)
async def not_confirm(message: Message):
    state_dispenser.set(
        message.peer_id,
        GeneralStates.MAIN_MENU,
        experience=None
    )
    await on_enter_share_experience(message)
