from aiogram.types import InlineKeyboardMarkup


def merge_inline_menus(first_menu: InlineKeyboardMarkup, second_menu: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        *first_menu.inline_keyboard,
        *second_menu.inline_keyboard,
    ])
