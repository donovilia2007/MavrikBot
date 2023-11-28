import random

from aiogram import types, F, Router, Dispatcher, Bot
from aiogram.types import Message, ContentType, ChatPermissions
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timedelta

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
        if (msg.reply_to_message == "None"):
            await msg.answer("Чтобы замутить пользователя, нужно ответить на его сообщение командой /mute")
        else:
            chat_id = msg.chat.id
            person_id = msg.from_user.id
            person = await bot.get_chat_member(chat_id, person_id)
            person_mute_id = msg.reply_to_message.from_user.id
            person_mute = await bot.get_chat_member(chat_id, person_mute_id)
            if (person_mute.status == "creator"):
                await msg.answer("С огнём шутки плохи...")
            else:
                if (person.can_restrict_members == True and person_mute.status == "member" or person.status == 'creator'):
                    if (person_mute.can_send_messages == False):
                        await msg.answer("Ау! Он уже замучен, слышишь?")
                    else:
                        sms = msg.text.split(" ")
                        permissions = ChatPermissions(can_send_messages=False, can_send_audios=False, can_send_documents=False, can_send_photos=False, can_send_videos=False, can_send_video_notes=False, can_send_voice_notes=False, can_send_polls=False, can_send_other_messages=False)
                        if (len(sms) == 1):
                            await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions, until_date=datetime.now() + timedelta(minutes=15))
                        elif (len(sms) == 3):
                            time = sms[1]
                            if (time.isdigit() == False):
                                await msg.answer("Ой ой, такого промежутка времени не существует")
                            else:
                                time = int(time)
                                if (sms[2] == "d"):
                                    await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions, until_date=datetime.now() + timedelta(days=time))
                                    if (time % 10 == 1 and time % 100 != 11):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} день", parse_mode="Markdown")
                                    elif ((time % 10 == 2 or time % 10 == 3 or time % 10 == 4) and time % 100 != 12 and time % 100 != 13 and time % 100 != 14):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} дня", parse_mode="Markdown")
                                    else:
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} дней", parse_mode="Markdown")
                                elif (sms[2] == "m"):
                                    await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions, until_date=datetime.now() + timedelta(minutes=time))
                                    if (time % 10 == 1 and time % 100 != 11):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} минуту", parse_mode="Markdown")
                                    elif ((time % 10 == 2 or time % 10 == 3 or time % 10 == 4) and time % 100 != 12 and time % 100 != 13 and time % 100 != 14):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} минуты", parse_mode="Markdown")
                                    else:
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} минут", parse_mode="Markdown")
                                elif (sms[2] == "h"):
                                    await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions, until_date=datetime.now() + timedelta(hours=time))
                                    if (time % 10 == 1 and time % 100 != 11):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} час", parse_mode="Markdown")
                                    elif ((time % 10 == 2 or time % 10 == 3 or time % 10 == 4) and time % 100 != 12 and time % 100 != 13 and time % 100 != 14):
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} часа", parse_mode="Markdown")
                                    else:
                                        await msg.answer(f"[{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) был лишён права голоса на {time} часов", parse_mode="Markdown")
                                else:
                                    await msg.answer(f"Я готов замутить [{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) на любое количество коточасов, но, к сожалению, я не знаю, сколько это😿", parse_mode="Markdown")
                else:
                    await msg.answer("Ты не можешь использовать эту команду!")

@router.message(Command("unmute"))
async def unmute(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Эту команду нельзя использовать в личных сообщениях")
    else:
        if (msg.reply_to_message == "None"):
            await msg.answer("Чтобы размутить пользователя, нужно ответить на его сообщение командой /unmute")
        else:
            chat_id = msg.chat.id
            person_id = msg.from_user.id
            person = await bot.get_chat_member(chat_id, person_id)
            person_mute_id = msg.reply_to_message.from_user.id
            person_mute = await bot.get_chat_member(chat_id, person_mute_id)
            if (person.can_restrict_members == "True" or person.status == "creator"):
                permissions = ChatPermissions(can_send_messages=True, can_send_audios=True, can_send_documents=True, can_send_photos=True, can_send_videos=True, can_send_video_notes=True, can_send_voice_notes=True, can_send_polls=True, can_send_other_messages=True)
                await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions)
                await msg.answer(f"Святые котики, [{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) снова может разговаривать! Но впредь, держи язык за зубами...", parse_mode="Markdown")

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