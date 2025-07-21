from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from settings import APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    description="VK Bot for museum",
    version=APP_VERSION
)


@app.get("/vk-bot/callback", response_class=PlainTextResponse)
def vk_confirmation():
    return "8b80bdd3"
