import os

from dotenv import load_dotenv

load_dotenv("./data/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PATH")
OWNER_ID = os.getenv("OWNER_ID")

if not BOT_TOKEN or not DATABASE_URL:
    raise ValueError("Заполните BOT_TOKEN и DATABASE_URL в data/.env")
