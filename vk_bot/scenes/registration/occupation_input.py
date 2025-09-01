from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from settings import state_dispenser
from actions.registration import submit_registration
from utils import get_state_payload


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_OCCUPATION)
    async def occupation_input_handler(message: Message):
        state_payload = await get_state_payload(state_dispenser, message.peer_id)
        state_payload.update({
            "occupation": message.text
        })
        await state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_OCCUPATION,
            **state_payload
        )
        await submit_registration(message, state_payload)
