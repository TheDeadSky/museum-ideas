from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MAIN_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить поддержку", callback_data="get_support")],
    [InlineKeyboardButton(text="Поделиться опытом", callback_data="share_experience")],
    [InlineKeyboardButton(text="Обратная связь", callback_data="feedback")],
    [InlineKeyboardButton(text="О проекте", callback_data="about_project")]
])

YES_NO_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да", callback_data="yes")],
    [InlineKeyboardButton(text="🚫 Нет", callback_data="no")],
])

CONFIRMATION_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")],
    [InlineKeyboardButton(text="Отмена", callback_data="not_confirm")],
])

SKIP_BUTTON = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пропустить", callback_data="skip")],
])

CANCEL_BUTTON = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
])

TO_MAIN_MENU_BUTTON = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В главное меню", callback_data="menu")],
])

GET_SUPPORT_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пройти курс самоподдержки", callback_data="self_support")],
    [InlineKeyboardButton(text="Узнать истории коллег", callback_data="colleagues_stories")],
])
