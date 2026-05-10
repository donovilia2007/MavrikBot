from aiogram import Router
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from start_aiogram import bot
from datetime import datetime, timedelta

router = Router()


async def can_user_mute(person, person_mute):
    return person.status == 'creator' or person.can_restrict_members and person_mute.status == 'member'


def CaseDays(time: int):
    if time % 10 == 1 and time % 100 != 11:
        return "день"

    if 2 <= time % 10 <= 4 and time // 10 % 10 != 1:
        return "дня"

    return "дней"


def CaseMinutes(time: int):
    if time % 10 == 1 and time % 100 != 11:
        return "минуту"

    if 2 <= time % 10 <= 4 and time // 10 % 10 != 1:
        return "минуты"

    return "минут"


def CaseHours(time: int):
    if time % 10 == 1 and time % 100 != 11:
        return "час"

    if 2 <= time % 10 <= 4 and time // 10 % 10 != 1:
        return "часа"

    return "часов"


class Administrator:
    mute_permissions = ChatPermissions(can_send_messages=False, can_send_audios=False,
                                       can_send_documents=False, can_send_photos=False,
                                       can_send_videos=False, can_send_video_notes=False,
                                       can_send_voice_notes=False, can_send_polls=False,
                                       can_send_other_messages=False, can_add_web_page_previews=False)

    @classmethod
    async def muteInMinutes(cls, chat_id, user, time):
        await bot.restrict_chat_member(chat_id=chat_id, user_id=user.user.id,
                                       permissions=cls.mute_permissions,
                                       until_date=datetime.now() + timedelta(minutes=time))

        minutes = CaseMinutes(time)

        await bot.send_message(chat_id=chat_id,
                               text=f"[{user.user.first_name}](tg://user?id={str(user.user.id)}) был лишён права голоса на {time} {minutes}",
                               parse_mode="Markdown")

    @classmethod
    async def muteInHours(cls, chat_id, user, time):
        await bot.restrict_chat_member(chat_id=chat_id, user_id=user.user.id,
                                       permissions=cls.mute_permissions,
                                       until_date=datetime.now() + timedelta(hours=time))

        hours = CaseHours(time)

        await bot.send_message(chat_id=chat_id,
                               text=f"[{user.user.first_name}](tg://user?id={str(user.user.id)}) был лишён права голоса на {time} {hours}",
                               parse_mode="Markdown")

    @classmethod
    async def muteInDays(cls, chat_id, user, time):
        await bot.restrict_chat_member(chat_id=chat_id, user_id=user.user.id,
                                       permissions=cls.mute_permissions,
                                       until_date=datetime.now() + timedelta(days=time))

        days = CaseDays(time)

        await bot.send_message(chat_id=chat_id,
                               text=f"[{user.user.first_name}](tg://user?id={str(user.user.id)}) был лишён права голоса на {time} {days}",
                               parse_mode="Markdown")

    @classmethod
    async def unmute(cls, chat_id, user):
        chat = await bot.get_chat(chat_id)
        permissions = chat.permissions

        await bot.restrict_chat_member(chat_id=chat_id, user_id=user.user.id, permissions=permissions)
        await bot.send_message(chat_id=chat_id,
                               text=f"Святые котики, [{user.user.first_name}](tg://user?id={str(user.user.id)}) снова может разговаривать! Но впредь, следи за языком...",
                               parse_mode="Markdown")


@router.message(Command("mute"))
async def mute(msg: Message):
    if msg.chat.type not in ["group", "supergroup"]:
        return await msg.answer("Эту команду нельзя использовать в личных сообщениях")

    if msg.reply_to_message is None:
        return await msg.answer("Чтобы замутить пользователя, нужно ответить на его сообщение командой /mute")

    chat_id = msg.chat.id
    person_id = msg.from_user.id
    person = await bot.get_chat_member(chat_id, person_id)
    person_mute_id = msg.reply_to_message.from_user.id
    person_mute = await bot.get_chat_member(chat_id, person_mute_id)

    if person_mute.status == "creator":
        return await msg.answer("С огнём шутки плохи...")

    if not await can_user_mute(person, person_mute):
        return await msg.answer("Ты не можешь использовать эту команду!")

    if person_mute.status == 'restricted' and not person_mute.can_send_messages:
        return await msg.answer("Пользователь уже замучен")

    message = msg.text.split()

    if len(message) == 1:
        return await Administrator.muteInMinutes(chat_id, person_mute, 15)

    elif len(message) == 3:
        time = message[1]
        type = message[2]

        if not time.isdigit():
            return await msg.answer("Ой ой, такого промежутка времени не существует")

        time = int(time)

        if type == 'm':
            return await Administrator.muteInMinutes(chat_id, person_mute, time)
        elif type == 'h':
            return await Administrator.muteInHours(chat_id, person_mute, time)
        elif type == 'd':
            return await Administrator.muteInDays(chat_id, person_mute, time)
        else:
            return await msg.answer(
                f"Я готов замутить [{person_mute.user.first_name}](tg://user?id={str(person_mute_id)}) на любое количество коточасов, но, к сожалению, я не знаю, сколько это😿",
                parse_mode="Markdown")

    return await msg.answer("Я тебя не понимаю")


@router.message(Command("unmute"))
async def unmute(msg: Message):
    if msg.chat.type not in ["group", "supergroup"]:
        return await msg.answer("Эту команду нельзя использовать в личных сообщениях")

    if msg.reply_to_message is None:
        return await msg.answer("Чтобы размутить пользователя, нужно ответить на его сообщение командой /unmute")

    chat_id = msg.chat.id
    person_id = msg.from_user.id
    person = await bot.get_chat_member(chat_id, person_id)
    person_mute_id = msg.reply_to_message.from_user.id
    person_mute = await bot.get_chat_member(chat_id, person_mute_id)

    if person.status == 'creator' or person.can_restrict_members == True:
        return await Administrator.unmute(chat_id, person_mute)

    return await msg.answer("Ты не можешь использовать эту команду!")
