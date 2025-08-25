from typing import Any

from vkbottle.bot import Message

from models.registration import RegistrationData
from services.api_service import get_text_from_db, register
from utils import make_one_button_menu
from actions.main_menu import default_main_menu
from settings import state_dispenser
from states.general_states import GeneralStates
from states.registration import Registration


def make_registration_button(button_text="Познакомиться", *, callback_data="registration"):
    return make_one_button_menu(button_text, callback_data)


async def submit_registration(message: Message, registration_data: dict[str, Any]):
    from_user = message.peer_id

    raw_data = {
        **registration_data,
        "vk_id": from_user
    }

    registration_data = RegistrationData(**raw_data)

    result = await register(registration_data)

    if result["success"]:
        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(message, main_menu_text=main_menu_text)

        state_dispenser.set(
            message.peer_id,
            GeneralStates.MAIN_MENU
        )
    else:
        state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_START
        )
        registration_button = make_registration_button("Попробовать снова")
        await message.answer(
            "Не удалось зарегистрироваться.",
            reply_markup=registration_button
        )
