import configparser

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from settings import APP_NAME, APP_VERSION

config = configparser.ConfigParser()
config.read("config.ini")

app = FastAPI(
    title=APP_NAME,
    description="VK Bot for museum",
    version=APP_VERSION
)


@app.post("/vk-bot/callback", response_class=PlainTextResponse)
async def vk_confirmation(request: Request):
    data = await request.json()
    print(data)

    with open("vk_response", "r") as file:
        return file.read()
