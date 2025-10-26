from fastapi.routing import APIRouter
from fastapi import Request, Response, status
from logs.logger import logger
from config.config import TELEGRAM_SECRET_TOKEN
from telegram import Update

router = APIRouter()

@router.post("/telegram")
async def telegram_webhook(request: Request):
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

@router.get('/')
async def index():
    return Response('ok', status_code=status.HTTP_200_OK)