from vkbottle import Keyboard
from vkbottle_schemas.keyboard import KeyboardButtonSchema


def make_yes_no_menu(swapped_icons: bool = False, for_state: str | None = None):
    if swapped_icons:
        yes_label = "🚫 Да"
        no_label = "✅ Нет"
    else:
        yes_label = "✅ Да"
        no_label = "🚫 Нет"
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label=yes_label,
            payload={"cmd": "yes", "state": for_state},
            type="callback"
        ).positive().get_json()],
        [KeyboardButtonSchema(
            label=no_label,
            payload={"cmd": "no", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_confirmation_menu(for_state: str):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Подтвердить", payload={"cmd": "confirm", "state": for_state},
            type="callback"
        ).positive().get_json()],
        [KeyboardButtonSchema(
            label="Отмена", payload={"cmd": "not_confirm", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()


def make_skip_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Пропустить", payload={"cmd": "skip", "state": for_state},
            type="callback"
        ).secondary().get_json()],
    ]).get_json()


def make_cancel_menu(for_state: str | None = None):
    return Keyboard(one_time=False, inline=True).schema([
        [KeyboardButtonSchema(
            label="Отмена", payload={"cmd": "cancel", "state": for_state},
            type="callback"
        ).negative().get_json()],
    ]).get_json()
