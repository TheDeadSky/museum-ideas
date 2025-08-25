from vkbottle.bot import Message, BotLabeler

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser
from menus import CONFIRMATION_MENU, YES_NO_MENU


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_NAME)
    async def name_input_handler(message: Message):
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_NAME_CONFIRMATION,
            firstname=message.text
        )
        name_confirmation_message = await get_text_from_db("name_confirmation_message")
        await message.answer(
            name_confirmation_message.format(message.text),
            keyboard=CONFIRMATION_MENU
        )

    @labeler.message(text="not_confirm", state=Registration.REGISTRATION_NAME_CONFIRMATION)
    async def not_confirm(message: Message):
        state_payload = message.state_peer.payload
        state_payload.update({
            "firstname": None
        })
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_NAME,
            **state_payload
        )
        await message.answer("Введите Ваше имя заново.")

    @labeler.message(text="confirm", state=Registration.REGISTRATION_NAME_CONFIRMATION)
    async def confirm(message: Message):
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_IS_MUSEUM_WORKER
        )
        is_museum_worker_question = await get_text_from_db("is_museum_worker_question")
        await message.answer(
            is_museum_worker_question,
            keyboard=YES_NO_MENU
        )
