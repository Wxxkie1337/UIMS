from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

from db import DataBase

router = Router()
database = DataBase()


class AppealStates(StatesGroup):
    category = State()
    custom_category = State()
    message = State()
    photo = State()
    location = State()
    finish = State()
