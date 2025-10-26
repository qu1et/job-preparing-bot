from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from telegram import Update
from bot_init import bot_init
from logs.logger import logger
from config.config import WEBHOOK_URL, TELEGRAM_PATH, TELEGRAM_SECRET_TOKEN
from server import telegram_router


def fastapi_init():
    app = FastAPI(lifespan=lifespan)
    app.include_router(telegram_router)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Тут что будет когда сервер поднимется
    bot_app = bot_init()

    app.state.bot_app = bot_app

    await bot_app.initialize()
    await bot_app.start()
    logger.info("Бот запущен ✅")
    await bot_app.bot.set_webhook(
        WEBHOOK_URL + TELEGRAM_PATH,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        secret_token=TELEGRAM_SECRET_TOKEN,
    )
    logger.info("Webhook установлен ✅")
    yield
    await bot_app.stop()
    logger.info("Бот остановлен ⚠️")
    await bot_app.bot.delete_webhook()
    logger.info("Webhook удален ⚠️")
    await bot_app.shutdown()
