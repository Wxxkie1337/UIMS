"""
Получаем данные из .env файла (токен бота, путь до базы данных)

Нужно создать .env по пути data/.env
Вид:
BOT_TOKEN=
DATABASE_PATH=
"""

import os
from dotenv import load_dotenv

load_dotenv("./data/.env")

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = os.getenv('DATABASE_PATH')

if not BOT_TOKEN or not DATABASE_PATH:
    raise ValueError("Заполните .env файл!")