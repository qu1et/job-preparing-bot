from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from telegram import Update
from bot_init import bot_init
import os


def fastapi_init():
    app = FastAPI(lifespan=lifespan)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Тут что будет когда сервер поднимется
    bot_app = bot_init()

    app.state.bot_app = bot_app

    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(
        os.getenv("WEBHOOK_URL") + os.getenv("TELEGRAM_PATH"),
        allowed_updates=Update.ALL_TYPES,
        drop_pendings_update=True,
        secret_token=os.getenv("TELEGRAM_SECRET_TOKEN"),
    )
    yield
    await bot_app.stop()
    await bot_app.bot.delete_webhook()
    await bot_app.shutdown()

    # что будет когда сервер положим
    @app.post("/telegram")
    def telegram_webhook(request: Request):
        if TELEGRAM_SECRET_TOKEN:
            header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if header_token != TELEGRAM_SECRET_TOKEN:
                logger.warning("Forbidden: invalid secret token header")
                return Response(status_code=status.HTTP_403_FORBIDDEN)

        try:
            payload = await request.json()
        except Exception:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        update = Update.de_json(payload, request.app.state.bot_app.bot)
        await request.app.state.bot_app.update_queue.put(update)
        return Response(status_code=status.HTTP_200_OK)
