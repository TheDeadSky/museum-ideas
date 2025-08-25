import aiohttp

from vkbottle import Keyboard
from vkbottle_schemas.keyboard import KeyboardButtonSchema


def merge_inline_menus(first_menu: Keyboard, second_menu: Keyboard) -> Keyboard:
    return Keyboard(one_time=True, inline=True).schema([
        *first_menu.buttons,
        *second_menu.buttons,
    ])


def make_one_button_menu(text: str, payload: str) -> Keyboard:
    return Keyboard(one_time=True, inline=True).schema([
        [KeyboardButtonSchema(label=text, payload=payload).primary().get_json()],
    ])


async def fetch_audio_binary(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Ошибка загрузки: HTTP {response.status}")
            return await response.read()
