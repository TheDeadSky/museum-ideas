import aiohttp
from typing import Any, Literal

from vkbottle import Keyboard, BuiltinStateDispenser
from vkbottle_schemas.keyboard import KeyboardButtonSchema


def merge_inline_menus(first_menu: Keyboard, second_menu: Keyboard) -> Keyboard:
    keyboard = Keyboard(one_time=False, inline=True)

    keyboard.buttons = [
        *first_menu.buttons,
        *second_menu.buttons
    ]

    return keyboard


def make_one_button_menu(
    text: str,
    payload: dict[str, Any],
    _type: Literal["text", "open_link", "callback", "location", "vkpay", "open_app"] = "callback"
) -> Keyboard:
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(label=text, payload=payload, type=_type).primary().get_json()],
    ])


async def fetch_audio_binary(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Ошибка загрузки: HTTP {response.status}")
            return await response.read()


async def get_state_payload(dispenser: BuiltinStateDispenser, peer_id: int):
    state_peer = await dispenser.get(peer_id)

    if state_peer is None:
        return {}

    return state_peer.payload
