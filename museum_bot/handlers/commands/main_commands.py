from aiogram import Router
from aiogram.fsm.scene import ScenesManager
from aiogram.filters import CommandStart
from aiogram.types import Message

from actions.main_menu import default_main_menu
from actions.registration import make_registration_button
from services.api_service import get_text_from_db, get_is_registered

mc_router = Router()


@mc_router.message(CommandStart())
async def command_start_handler(message: Message, scenes: ScenesManager) -> None:
    await scenes.close()

    result = await get_is_registered(str(message.from_user.id))
    is_registered = result["is_registered"]

    if is_registered:
        await default_main_menu(
            message,
            get_text_from_db("main_menu_text")
        )
        return

    greetings = await get_text_from_db("start_greetings")

    await message.answer(greetings, reply_markup=make_registration_button())
