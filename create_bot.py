from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from data.bd import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename='.env'), encoding="utf-8", override=True)
TOKEN = os.environ.get('TOKENTEST')
CHAT_ID = os.environ.get('CHAT_ID')
ADMIN_ID = os.environ.get('ADMIN_ID')

db = DataBase('data/database.db')

bot: Bot = Bot(token=TOKEN)

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
