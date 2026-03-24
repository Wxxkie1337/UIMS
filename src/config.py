"""
BOT_TOKEN - токен бота
DATABASE_URL - ссылка на базу данных postgresql
REDIS_URL - ссылка на redis
OWNERS_ID - id владельцев бота (LIST[INT])
BOT_USER - username бота из телеграма
"""


import os

from dotenv import load_dotenv
from utils.messages import CONFIG_ENV_ERROR
from ast import literal_eval

load_dotenv("./data/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PATH")
REDIS_URL = os.getenv("REDIS_URL")
OWNERS_ID = literal_eval(os.getenv("OWNERS_ID"))
BOT_USER = os.getenv("BOT_USER")

if not BOT_TOKEN or not DATABASE_URL:
    raise ValueError(CONFIG_ENV_ERROR)
