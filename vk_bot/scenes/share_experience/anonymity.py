import logging
from vkbottle.bot import BotLabeler, Message

from actions.share_experience import submit_share_experience
from states.share_experience import ShareExperienceStates
from settings import state_dispenser


experience_anonymity_labeler = BotLabeler()


@experience_anonymity_labeler.callback_query(payload="yes", state=ShareExperienceStates.ANONYMITY)
@experience_anonymity_labeler.callback_query(payload="no", state=ShareExperienceStates.ANONYMITY)
async def handle_anonymous(message: Message):
    logging.info(message.payload)
    state_payload = message.state_peer.payload
    state_payload.update({
        "is_anonymous": message.payload == "yes"
    })
    state_dispenser.set(
        message.peer_id,
        ShareExperienceStates.ANONYMITY,
        **state_payload
    )
    await submit_share_experience(message, state_payload)
