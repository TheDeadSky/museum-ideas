from utils import make_one_button_menu


def make_registration_button(button_text="Познакомиться", *, callback_data="registration"):
    return make_one_button_menu(button_text, callback_data)
