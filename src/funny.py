import random
import aiosqlite

from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from start_aiogram import bot

router = Router()

with open("stickers.txt", "r", encoding="utf-8") as file:
    stickers = file.read().splitlines()

@router.message()
async def ordinary_message(msg: Message):
    """
    Обрабатывает обычные сообщения.
    """
    text = msg.text.lower()
    if "мур" in text or "мяу" in text:
        await msg.answer_sticker(random.choice(stickers))