import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TELEGRAM_PATH = os.getenv("TELEGRAM_PATH")
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")
SHOP_ID = os.getenv("SHOP_ID")
SECRET_KEY_YOUKASSA = os.getenv("SECRET_KEY_YOUKASSA")
PRICE = os.getenv("PRICE")
