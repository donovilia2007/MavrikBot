from aiogram import Router, Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()
f = open("../TOKEN.txt")
token = f.read()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=token)