import random


from aiogram import types, F, Router, Dispatcher, Bot
from aiogram.types import Message, ContentType, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timedelta

router = Router()
f = open("TOKEN.txt")
token = f.read()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=token)

santa_dict = {}

with open("stickers.txt") as file:
    stickers = file.readline().split(',')

@router.message(Command("start"))
async def start_message(msg: Message):
    text = msg.text.split(" ")
    user = msg.from_user.id
    if len(text) > 1:
        text = [text[0]] + text[1].split('-')
        key = '-100' + text[1]
        ms_key = text[2]
        if key in santa_dict and msg.chat.type == "private":
            chat = await bot.get_chat(key)
            if user in santa_dict[key]:
                await msg.answer("Ты уже играешь!")
            else:
                santa_dict[key].append(user)
                await msg.answer(f"🎄Ты присоединился к игре в чате *{chat.title}*", parse_mode="Markdown")
                sms = "Хо-хо-хо! А кто это у нас решил поиграть в тайного санту?🎅\n\nИграют:\n"
                for i in range(0, len(santa_dict[key])):
                    person = await bot.get_chat_member(chat_id=key, user_id=santa_dict[key][i])
                    sms += f"{i + 1}. [{person.user.first_name}](tg://user?id={person.user.id})\n"
                    button = InlineKeyboardButton(text="Хочу быть Сантой", url=f"t.me/Mavrik_my_Bot?start={key[4:]}-{ms_key}")
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
                await bot.edit_message_text(chat_id=key, message_id=ms_key, text=sms, parse_mode="Markdown", reply_markup=keyboard)
        else:
            await msg.answer("Ай-ай, шалунишка!")
        return
    await msg.answer("Привет! Меня зовут Маврик! Я маленький добренький котик, живущий самой обычной жизнью) Надеюсь, мы подружимся!😸❤️\n\nНе забудь подписаться на официальный канал -> @How_Mavrik_was_made")



@router.message(Command("mute"))
async def mute(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Эту команду нельзя использовать в личных сообщениях")
    else:
        if (msg.reply_to_message == None):
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
                        permissions = ChatPermissions(can_send_messages=False, can_send_audios=False, can_send_documents=False, can_send_photos=False, can_send_videos=False, can_send_video_notes=False, can_send_voice_notes=False, can_send_polls=False, can_send_other_messages=False, can_add_web_page_previews=False)
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
                            await msg.answer("Я тебя совсем не понимаю...")
                else:
                    await msg.answer("Ты не можешь использовать эту команду!")

@router.message(Command("unmute"))
async def unmute(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Эту команду нельзя использовать в личных сообщениях")
    else:
        if (msg.reply_to_message == None):
            await msg.answer("Чтобы размутить пользователя, нужно ответить на его сообщение командой /unmute")
        else:
            chat_id = msg.chat.id
            person_id = msg.from_user.id
            person = await bot.get_chat_member(chat_id, person_id)
            person_mute_id = msg.reply_to_message.from_user.id
            person_mute = await bot.get_chat_member(chat_id, person_mute_id)
            if (person.can_restrict_members == "True" or person.status == "creator"):
                permissions = ChatPermissions(can_send_messages=True, can_send_audios=True, can_send_documents=True, can_send_photos=True, can_send_videos=True, can_send_video_notes=True, can_send_voice_notes=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True)
                await bot.restrict_chat_member(chat_id=chat_id, user_id=person_mute_id, permissions=permissions)
                await msg.answer(f"Святые котики, [{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) снова может разговаривать! Но впредь, держи язык за зубами...", parse_mode="Markdown")
            else:
                await msg.answer("Мне кажется, ты не можешь использовать эту команду")

@router.message(Command("santa"))
async def santa(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Я бы с радостью подарил тебе 10 подарочков, но, к сожалению, команду можно использовать только в групповых чатах")
        return
    else:
        chat_id = str(msg.chat.id)
        person_id = msg.from_user.id
        person = await bot.get_chat_member(chat_id, person_id)
        if person.status != "administrator" and person.status != "creator":
            await msg.answer("У тебя недостаточно прав")
            return
        ch_id = chat_id[4:]
        if chat_id in santa_dict:
            await msg.reply("Распределение тайных сант уже запущено!")
            return
        button = InlineKeyboardButton(text="Хочу быть Сантой", url=f"t.me/Mavrik_my_Bot?start={ch_id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        santa_dict[chat_id] = []
        mes = await msg.answer("Хо-хо-хо! А кто это у нас решил поиграть в тайного санту?🎅", reply_markup=keyboard)
        mes_id = mes.message_id
        button = InlineKeyboardButton(text="Хочу быть Сантой", url=f"t.me/Mavrik_my_Bot?start={ch_id}-{mes_id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=mes_id, reply_markup=keyboard)

@router.message(Command("start_santa"))
async def hey_santa(msg: Message):
    if (msg.chat.type != "supergroup"):
        await msg.answer("Эта команда не может быть запущена в личных сообщениях!")
        return
    else:
        chat_id = str(msg.chat.id)
        person_id = msg.from_user.id
        person = await bot.get_chat_member(chat_id, person_id)
        if person.status != "administrator" and person.status != "creator":
            await msg.answer("У тебя недостаточно прав")
            return
        if chat_id in santa_dict:
            mas = santa_dict[chat_id]
            mas2 = list(mas)
            flag = True
            while flag:
                random.shuffle(mas2)
                k = 0
                for i in range(0, len(mas)):
                    if mas[i] == mas2[i]:
                        k += 1
                        break
                if k == 0:
                    flag = False
                    break
            for i in range(0, len(mas)):
                prs_id = mas[i]
                prs2_id = mas2[i]
                prs2 = await bot.get_chat(prs2_id)
                await bot.send_message(chat_id=prs_id, text=f"🎇Хо-хо! На этот Новый Год ты становишься тайным сантой для [{prs2.first_name}](tg://user?id={prs2.id})", parse_mode="Markdown")
            sms = "🎁Жеребьёвка окончена! Тайными Сантами стали:\n"
            for i in range(0, len(mas)):
                person = await bot.get_chat_member(chat_id=chat_id, user_id=santa_dict[chat_id][i])
                sms += f"{i + 1}. [{person.user.first_name}](tg://user?id={person.user.id})\n"
            await msg.answer(text=sms, parse_mode="Markdown")
            del santa_dict[chat_id]
        else:
            await msg.answer("В этом чате ещё не проводилась жеребьёвка. Чтобы её запустить, администратор чата должен вызвать команду /santa")
@router.message(F.new_chat_members)
async def hello_new_person(msg: Message):
    new_member = msg.new_chat_members[0]
    await msg.answer(f"Привет [{new_member.first_name}](tg://user?id={str(new_member.id)})! Добро пожаловать в этот уютный чатик!\n\nРасскажи о себе, чтобы поскорее познакомиться со всеми😸", parse_mode="Markdown")
@router.message()
async def text_answer(msg: Message):
    if (msg.text == None):
        return
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