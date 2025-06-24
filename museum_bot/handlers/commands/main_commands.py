from aiogram import Router
from aiogram.fsm.scene import ScenesManager
from aiogram.filters import CommandStart
from aiogram.types import Message

from actions.main_menu import default_main_menu
from menus import REGISTER_BUTTON
from services.api_service import get_text_from_db

mc_router = Router()


@mc_router.message(CommandStart())
async def command_start_handler(message: Message, scenes: ScenesManager) -> None:
    greetings = await get_text_from_db("start_greetings")  # TODO: get from API
    description = await get_text_from_db("about_project_text")  # TODO: get from API
    is_registered = False  # get from API

    await message.answer(greetings)
    await message.answer(description)

    if is_registered:
        await default_main_menu(message)

    else:
        await scenes.close()
        await message.answer("Вы не зарегистрированы", reply_markup=REGISTER_BUTTON)
