from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_registration_button(button_text="Познакомиться", *, callback_data="registration"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, callback_data=callback_data)],
    ])
