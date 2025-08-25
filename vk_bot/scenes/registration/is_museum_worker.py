from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser
from menus import SKIP_BUTTON


def init(labeler: BotLabeler):
    @labeler.message(text="yes", state=Registration.REGISTRATION_IS_MUSEUM_WORKER)
    async def yes(message: Message):
        state_payload = message.state_peer.payload
        state_payload.update({
            "is_museum_worker": True
        })
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_WHICH_MUSEUM,
            **state_payload
        )
        which_museum_question = await get_text_from_db("which_museum_question")
        await message.answer(
            which_museum_question,
            keyboard=SKIP_BUTTON
        )

    @labeler.message(text="no", state=Registration.REGISTRATION_IS_MUSEUM_WORKER)
    async def no(message: Message):
        state_payload = message.state_peer.payload
        state_payload.update({
            "is_museum_worker": False
        })
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_OCCUPATION,
            **state_payload
        )
        sphere_of_activity_question = await get_text_from_db("sphere_of_activity_question")
        await message.answer(sphere_of_activity_question)
