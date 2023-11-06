import random

from aiogram import types, F, Router
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode

router = Router()

with open("stickers.txt") as file:
    stickers = file.readline().split(',')
@router.message(Command("start"))
async def start_message(msg: Message):
    await msg.answer("Привет! Меня зовут Маврик! Я маленький добренький котик, живущий самой обычной жизнью) Надеюсь, мы подружимся!😸❤️\n\nНе забудь подписаться на официальный канал -> @How_Mavrik_was_made")

@router.message(F.new_chat_members)
async def hello_new_person(msg: Message):
    new_member = msg.new_chat_members[0]
    await msg.answer(f"Привет [{new_member.first_name}](tg://user?id={str(new_member.id)})! Добро пожаловать в этот уютный чатик!\n\nРасскажи о себе, чтобы поскорее познакомиться со всеми😸", parse_mode="Markdown")

@router.message()
async def sticker_answer(msg: Message):
    text = msg.text.lower()
    if (text == "мур" or text == "мяу"):
        await msg.answer_sticker(random.choice(stickers))
