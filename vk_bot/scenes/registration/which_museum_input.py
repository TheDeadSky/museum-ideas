from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from settings import state_dispenser
from actions.registration import submit_registration


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_WHICH_MUSEUM)
    async def museum_input_handler(message: Message):
        state_payload = message.state_peer.payload
        state_payload.update({
            "museum": message.text
        })
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        await submit_registration(message, state_payload)

    @labeler.message(text="skip", state=Registration.REGISTRATION_WHICH_MUSEUM)
    async def skip_museum_question(message: Message):
        state_payload = message.state_peer.payload
        state_payload.update({
            "museum": None
        })
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        await submit_registration(message, state_payload)
