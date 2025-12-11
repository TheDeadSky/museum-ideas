import logging

from contextlib import asynccontextmanager
from fastapi.responses import PlainTextResponse

from bot import bot
from fastapi import BackgroundTasks, FastAPI, Request, Response

from bot_actions_api.bot_actions_routes import vk_bot_actions_router

confirmation_code: str = ""
secret_key: str = ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Setup webhook")
    global confirmation_code, secret_key
    confirmation_code, secret_key = await bot.setup_webhook()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(vk_bot_actions_router)


@app.get("/health")
async def health():
    return Response("ok")


@app.post("/vk-bot/callback", response_class=PlainTextResponse)
async def vk_handler(req: Request, background_task: BackgroundTasks):
    data = await req.json()
    logging.info(f"data: {data}")
    try:
        data = await req.json()
    except Exception:
        logging.warning("Empty request")
        return Response("not today", status_code=403)

    if data["type"] == "confirmation":
        logging.info("Send confirmation token: {}", confirmation_code)
        return Response(confirmation_code)

    if data["secret"] == secret_key:
        background_task.add_task(bot.process_event, data)
    return Response("ok")
