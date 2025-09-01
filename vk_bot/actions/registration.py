from typing import Any

from vkbottle.bot import Message, MessageEvent

from models.registration import RegistrationData
from services.api_service import get_text_from_db, register
from utils import make_one_button_menu
from actions.main_menu import default_main_menu
from settings import state_dispenser
from states.general_states import GeneralStates
from states.registration import Registration


def make_registration_button(button_text="Познакомиться", **kwargs):
    callback_data = kwargs.get("callback_data", {"cmd": "registration", "state": Registration.REGISTRATION_START.value})
    return make_one_button_menu(button_text, callback_data)


async def submit_registration(message: Message | MessageEvent, registration_data: dict[str, Any]):
    raw_data = {
        **registration_data,
        "vk_id": str(message.peer_id)
    }

    registration_data_object = RegistrationData(**raw_data)

    result = await register(registration_data_object)

    if result["success"]:
        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(message, main_menu_text=main_menu_text)

        await state_dispenser.set(
            message.peer_id,
            GeneralStates.MAIN_MENU
        )
    else:
        await state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_START
        )
        registration_button = make_registration_button("Попробовать снова").get_json()

        if isinstance(message, Message):
            await message.answer(
                "Не удалось зарегистрироваться.",
                keyboard=registration_button
            )
        else:
            await message.send_message(
                "Не удалось зарегистрироваться.",
                keyboard=registration_button
            )
