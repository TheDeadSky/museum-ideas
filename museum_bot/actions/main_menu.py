from aiogram.types import Message

from menus import MAIN_MENU


async def default_main_menu(message: Message, main_menu_text: str = "Главное меню"):
    await message.answer(main_menu_text, reply_markup=MAIN_MENU)
