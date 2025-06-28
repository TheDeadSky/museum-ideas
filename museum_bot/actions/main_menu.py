import os
import json

from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from menus import MAIN_MENU


async def default_main_menu(message: Message, main_menu_text: str = "Главное меню"):

    if os.path.exists("templates/main_menu.json"):
        with open("templates/main_menu.json", "r") as f:
            main_menu_data = json.load(f)

        if main_menu_data:
            buttons = [
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=button["callback_data"]
                ) for button in main_menu_data["buttons"]
            ]
            await message.answer(main_menu_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
        else:
            await message.answer(main_menu_text, reply_markup=MAIN_MENU)
    else:
        await message.answer(main_menu_text, reply_markup=MAIN_MENU)
