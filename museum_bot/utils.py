from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def merge_inline_menus(first_menu: InlineKeyboardMarkup, second_menu: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        *first_menu.inline_keyboard,
        *second_menu.inline_keyboard,
    ])


def escape_tg_reserved_characters(text: str) -> str:
    """
    Escapes specific characters in text with double backslashes.

    Args:
        text (str): The input text to escape characters in

    Returns:
        str: Text with escaped characters
    """
    characters_to_escape = ['.', '!', '?', '=', '/', '-', '(', ')']

    for char in characters_to_escape:
        text = text.replace(char, f'\\{char}')

    return text


def make_one_button_menu(text: str, callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=callback_data)],
    ])
