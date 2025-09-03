import os
from vkbottle import API, BuiltinStateDispenser, VoiceMessageUploader
from vkbottle.bot import BotLabeler
from vkbottle.callback import BotCallback

APP_NAME = "Museum VK Bot"
APP_VERSION = "1.0.0"
TOKEN = os.getenv("VK_BOT_TOKEN")
GROUP_ID = int(os.getenv("VK_GROUP_ID", "0"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/vk-bot/callback")
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", "9001"))
VK_SECRET_KEY = os.getenv("VK_SECRET_KEY", "")
VK_CONFIRMATION_CODE = os.getenv("VK_CONFIRMATION_CODE", "")


if TOKEN is None:
    raise RuntimeError("VK_BOT_TOKEN not found")

api = API(TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
voice_uploader = VoiceMessageUploader(
    api=api
)
callback = BotCallback(
    url="https://deadsky-dev.ru/vk-bot/callback",
    title="my server",
    secret_key=VK_SECRET_KEY,
    api=api
)
