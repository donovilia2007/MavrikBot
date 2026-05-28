from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

f = open("TOKEN.txt")
token = f.read()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=token)