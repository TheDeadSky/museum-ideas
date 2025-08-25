from vkbottle.bot import BotLabeler, Message

from actions.main_menu import default_main_menu
from services.api_service import get_text_from_db


main_menu_labeler = BotLabeler()


@main_menu_labeler.message(text="меню")
@main_menu_labeler.message(command="/menu")
async def on_main_menu_handler(self, message: Message):
    main_menu_text = await get_text_from_db("main_menu_text")
    await default_main_menu(message, main_menu_text=main_menu_text)


@main_menu_labeler.message(payload="main_menu")
async def on_main_menu_callback_handler(self, message: Message):
    main_menu_text = await get_text_from_db("main_menu_text")
    await default_main_menu(message, main_menu_text=main_menu_text)


__all__ = ["main_menu_labeler"]
