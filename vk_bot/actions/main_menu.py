import os
import json
from vkbottle import Keyboard, Text
from vkbottle.bot import Message

from menus import MAIN_MENU


async def default_main_menu(message: Message, main_menu_text: str = "Главное меню", *, mode: str = "prod"):
    if os.path.exists("templates/main_menu.json"):
        with open("templates/main_menu.json", "r") as f:
            main_menu_data = json.load(f)

        if main_menu_data:
            ordered_buttons = sorted(main_menu_data["buttons"], key=lambda x: x["order"])
            keyboard = Keyboard(one_time=True, inline=True)

            for button in ordered_buttons:
                if mode in button["modes"]:
                    keyboard.add(Text(button["text"]), payload={"cmd": button["callback_data"]})

            await message.answer(main_menu_text, keyboard=keyboard.get_json())
        else:
            await message.answer(main_menu_text, keyboard=MAIN_MENU)
    else:
        await message.answer(main_menu_text, keyboard=MAIN_MENU)
