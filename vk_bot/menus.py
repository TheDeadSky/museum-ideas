from vkbottle import Keyboard
from vkbottle_schemas.keyboard import KeyboardButtonSchema

MAIN_MENU = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Получить поддержку", payload="get_support").primary().get_json()],
    [KeyboardButtonSchema(label="Поделиться опытом", payload="share_experience").primary().get_json()],
    [KeyboardButtonSchema(label="Обратная связь", payload="feedback").primary().get_json()],
    [KeyboardButtonSchema(label="О проекте", payload="about_project").secondary().get_json()],
]).get_json()

YES_NO_MENU = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="✅ Да", payload="yes").positive().get_json()],
    [KeyboardButtonSchema(label="🚫 Нет", payload="no").negative().get_json()],
]).get_json()

YES_NO_MENU_SWAPPED_ICONS = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="🚫 Да", payload="yes").positive().get_json()],
    [KeyboardButtonSchema(label="✅ Нет", payload="no").negative().get_json()],
]).get_json()


CONFIRMATION_MENU = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Подтвердить", payload="confirm").positive().get_json()],
    [KeyboardButtonSchema(label="Отмена", payload="not_confirm").negative().get_json()],
]).get_json()

SKIP_BUTTON = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Пропустить", payload="skip").secondary().get_json()],
]).get_json()

CANCEL_BUTTON = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Отмена", payload="cancel").negative().get_json()],
]).get_json()

TO_MAIN_MENU_BUTTON = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="В главное меню", payload="menu").primary().get_json()],
]).get_json()

GET_SUPPORT_MENU = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Пройти курс самоподдержки", payload="self_support").primary().get_json()],
    [KeyboardButtonSchema(label="Узнать истории коллег", payload="colleagues_stories").primary().get_json()],
]).get_json()

ONE_MORE_STORY_BUTTON = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(label="Узнать еще одну историю", payload="one_more_story").primary().get_json()],
]).get_json()

NEXT_PART_BUTTON = Keyboard(one_time=True, inline=True).schema([
    [KeyboardButtonSchema(
        label="Смотреть следующую лекцию", payload="self_support_next_part"
    ).primary().get_json()],
]).get_json()
