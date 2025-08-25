from vkbottle.bot import BotLabeler, Message

from actions.share_experience import submit_share_experience
from states.share_experience import ShareExperienceStates
from settings import state_dispenser
from menus import YES_NO_MENU_SWAPPED_ICONS
from services.api_service import get_text_from_db

experience_publishing_labeler = BotLabeler()


@experience_publishing_labeler.message(payload="yes")
async def publish_yes(message: Message):
    state_payload = message.state_peer.payload
    state_payload.update({
        "publish": True
    })
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    anonymous_question = await get_text_from_db("anonymous_message_question")
    await message.answer(
        anonymous_question,
        keyboard=YES_NO_MENU_SWAPPED_ICONS
    )


@experience_publishing_labeler.message(payload="no")
async def publish_no(message: Message):
    state_payload = message.state_peer.payload
    state_payload.update({
        "publish": False,
        "anonymous": True
    })
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    await submit_share_experience(message, state_payload)
