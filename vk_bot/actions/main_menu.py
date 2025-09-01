import os
import json

from typing import overload

from vkbottle import Keyboard, Callback
from vkbottle_schemas.keyboard import KeyboardButtonSchema
from vkbottle.bot import Message, MessageEvent

from menus import MAIN_MENU


@overload
async def default_main_menu(obj: Message, main_menu_text: str = "Главное меню", *, mode: str = "prod") -> None: ...


@overload
async def default_main_menu(obj: MessageEvent, main_menu_text: str = "Главное меню", *, mode: str = "prod") -> None: ...


async def default_main_menu(
    obj: Message | MessageEvent,
    main_menu_text: str = "Главное меню",
    *,
    mode: str = "prod"
) -> None:
    send_method = obj.answer if isinstance(obj, Message) else obj.send_message

    if os.path.exists("templates/main_menu.json"):
        with open("templates/main_menu.json", "r") as f:
            main_menu_data = json.load(f)

        if main_menu_data:
            ordered_buttons = sorted(main_menu_data["buttons"], key=lambda x: x["order"])
            keyboard = Keyboard(one_time=False, inline=True)

            for button in ordered_buttons:
                if mode in button["modes"]:
                    keyboard.add(Callback(button["text"], payload=button["callback_data"])).row()

            await send_method(main_menu_text, keyboard=keyboard.get_json())
            return

    await send_method(main_menu_text, keyboard=MAIN_MENU.get_json())


def make_to_main_menu_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="В главное меню", payload={"cmd": "main_menu", "state": for_state},
            type="callback"
        ).primary().get_json()],
    ]).get_json()
