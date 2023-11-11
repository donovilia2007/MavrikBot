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
    if ("мур" in text or "мяу" in text):
        await msg.answer_sticker(random.choice(stickers))
    command = text.split(' ')
    if (command[0] == "вероятность"):
        rand = random.randint(1, 5)
        if rand == 1:
            await msg.answer(f"🧙🏻‍♂️Святой Амур говорит {random.randint(1, 100)}%")
        elif rand == 2:
            await msg.answer(f"🐈Мяу! Да здесь все {random.randint(1, 100)}%")
        elif rand == 3:
            await msg.answer(f"Может быть {random.randint(1, 100)}%, а может и нет😜")
        elif rand == 4:
            await msg.answer(f"Глубоко проанализировав данный вопрос, а также изучив необходимый материал, с вероятностью {random.randint(1, 100)}% я могу заявить, что это правда🤓")
        elif rand == 5:
            await msg.answer(f"🕊Птичка нашептала, что {random.randint(1, 100)}%")