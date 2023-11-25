import random
from aiogram import types, F, Router, Dispatcher, Bot
from aiogram.types import Message, ContentType, Chat
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()
f = open("TOKEN.txt")
token = f.read()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=token, parse_mode=ParseMode.HTML)

with open("stickers.txt") as file:
    stickers = file.readline().split(',')

@router.message(Command("start"))
async def start_message(msg: Message):
    await msg.answer("Привет! Меня зовут Маврик! Я маленький добренький котик, живущий самой обычной жизнью) Надеюсь, мы подружимся!😸❤️\n\nНе забудь подписаться на официальный канал -> @How_Mavrik_was_made")

@router.message(Command("mute"))
async def mute(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Эту команду нельзя использовать в личных сообщениях")
    else:
        chat_id = msg.chat.id
        person_id = msg.from_user.id
        person = await bot.get_chat_member(chat_id, person_id)
        if (person.can_restrict_members == True or person.status == 'creator'):
                sms = msg.text.split(" ")
                await msg.answer("К сожалению, функционал этой команды пока не доступен. Следить за обновлениями можно в официальном канале -> @How_Mavrik_was_made")
                #await bot.restrict_chat_member()
        else:
            await msg.answer("Ты не можешь использовать эту команду!")
@router.message(F.new_chat_members)
async def hello_new_person(msg: Message):
    new_member = msg.new_chat_members[0]
    await msg.answer(f"Привет [{new_member.first_name}](tg://user?id={str(new_member.id)})! Добро пожаловать в этот уютный чатик!\n\nРасскажи о себе, чтобы поскорее познакомиться со всеми😸", parse_mode="Markdown")

@router.message()
async def text_answer(msg: Message):
    text = msg.text.lower()
    if (text == "пинг"):
        await msg.answer("ПОНГ🏓")
    if (text == "динь"):
        await msg.answer("ДОН🔔")
    if (text == "бум"):
        await msg.answer("БОМ🥁")
    if (text == "💃"):
        await msg.answer("Танцуй!🕺")
    if (text == "🎤"):
        await msg.answer("МЯУ-МЯУ-МЯУ-МЯЯЯЯЯУ!🎶")
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