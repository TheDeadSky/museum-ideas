import logging
from os import getenv

from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from handlers.commands.main_commands import mc_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from scenes.registration import registration_scenes_router, registration_scenes_registry
from scenes.main_menu import main_menu_router, main_menu_scenes_registry
from scenes.get_support import get_support_router, get_support_scenes_registry
from scenes.share_experience import share_experience_router, share_experience_scenes_registry

TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")
WEBHOOK_PATH = getenv("WEBHOOK_PATH", "/webhook")
WEBAPP_HOST = getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(getenv("WEBAPP_PORT", "3000"))


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{WEBHOOK_URL}",
        secret_token="ad23wad5sg4fg5bdf1s2vda5wca5s445ca",
    )


def main() -> None:
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )

    scenes_registry = SceneRegistry(dispatcher)

    scenes_registry.add(
        *registration_scenes_registry,
        *main_menu_scenes_registry,
        *get_support_scenes_registry,
        *share_experience_scenes_registry,
    )

    dispatcher.include_routers(
        mc_router,
        registration_scenes_router,
        main_menu_router,
        get_support_router,
        share_experience_router,
    )

    dispatcher.startup.register(on_startup)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    app = web.Application()

    webhook_handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dispatcher, bot=bot)

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
