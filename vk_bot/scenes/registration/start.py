from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser


def init(labeler: BotLabeler):
    @labeler.message(payload={"cmd": "registration"}, state=Registration.REGISTRATION_START)
    async def start_registration(message: Message):
        name_question = await get_text_from_db("name_question")
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_NAME
        )
        await message.answer(name_question)
