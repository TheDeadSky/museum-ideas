from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MAIN_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить поддержку", callback_data="get_support")],
    [InlineKeyboardButton(text="Поделиться опытом", callback_data="share_experience")],
    # [InlineKeyboardButton(text="Обратная связь", callback_data="feedback")],
    [InlineKeyboardButton(text="О проекте", callback_data="about_project")]
])

YES_NO_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да", callback_data="yes")],
    [InlineKeyboardButton(text="🚫 Нет", callback_data="no")],
])

YES_NO_MENU_SWAPPED_ICONS = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚫 Да", callback_data="yes")],
    [InlineKeyboardButton(text="✅ Нет", callback_data="no")],
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
    [InlineKeyboardButton(text="Присоединиться к онлайн-встречам", callback_data="join_online_meetup")]
])

ONE_MORE_STORY_BUTTON = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Узнать еще одну историю", callback_data="one_more_story")],
])

NEXT_PART_BUTTON = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Смотреть следующую лекцию", callback_data="self_support_next_part")],
])

JOIN_ONLINE_MEETUP_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перейти", url="https://t.me/+dBiLytf_PzZkOGRi")],
    [InlineKeyboardButton(text="Нет", callback_data="no")]
])
