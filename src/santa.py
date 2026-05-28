import random
import aiosqlite

from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from start_aiogram import bot

router = Router()


class SantaGame:
    """
    SantaGame --- класс, который отвечает за базу данных со всеми играми в Тайного Санту.

    Имеет атрибут db --- расположение базы данных.
    """
    db = "santa.db"

    @classmethod
    async def init_db(cls):
        """
        Инициализирует базу данных.

        Не принимает аргументов.

        Ничего не возвращает.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS participants
                                (chat_id TEXT, user_id INTEGER, recipient_id INTEGER, 
                                PRIMARY KEY (chat_id, user_id))''')
            await db.commit()

    @classmethod
    async def add_player(cls, chat_id: int | str, user_id: int | str):
        """
        Добавляет пользователя в игру.

        Принимает chat_id и user_id --- id группы, в которой ведётся игра и id пользователя, который хочет вступить в игру.

        Возвращает bool --- удалось ли пользователя в игру.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            try:
                await db.execute('''INSERT INTO participants (chat_id, user_id)
                                    VALUES (?, ?)''', (str(chat_id), str(user_id)))
                await db.commit()
                return True
            except:
                return False

    @classmethod
    async def remove_player(cls, chat_id: int | str, user_id: int | str):
        """
        Удаляет пользователя из игры.

        Принимает chat_id и user_id --- id группы, в которой ведётся игра и id пользователя, который хочет выйти из игры.

        Возвращает bool --- удалось ли удалить пользователя из игры.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            try:
                await db.execute('''DELETE FROM participants 
                                    WHERE chat_id = ? AND user_id = ?''',
                                 (str(chat_id), str(user_id)))
                await db.commit()
                return True
            except:
                return False

    @classmethod
    async def get_player_games(cls, user_id: int | str):
        """
        Получает все игры для конкретного пользователя.

        Принимает user_id --- id пользователя.

        Возвращает list comprehension --- список пар {chat_id, recipient_id},
        где chat_id --- id группы, в которой пользователь играет в Тайного Санту, и recipient_it --- получатель подарка от пользователя.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            async with db.execute('''SELECT chat_id, recipient_id FROM participants
                                     WHERE user_id = ?''', (str(user_id),)) as cursor:
                pairs = await cursor.fetchall()
                return [[pair[0], pair[1]] for pair in pairs]

    @classmethod
    async def get_players(cls, chat_id: int | str):
        """
        Получает список игроков в группе.

        Принимает chat_id --- id группы, в которой ведётся игра.

        Возвращает list comprehension --- список игроков.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            async with db.execute('''SELECT user_id FROM participants 
                                     WHERE chat_id = ?''',
                                  (str(chat_id),)) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    @classmethod
    async def make_draw(cls, chat_id: int | str):
        """
        Начинает жеребьёвку в чате.

        Принимает chat_id --- id группы, в которой ведётся игра.

        Возвращает None, если игроков в группе меньше 3.

        Возвращает list --- список пар вида {player, recipient}, где player --- даритель подарка, recipient --- получатель подарка.

        Является @classmethod.
        """
        players = await cls.get_players(chat_id)

        if len(players) <= 2:
            return None

        recipients = players.copy()

        while True:
            random.shuffle(recipients)
            if all(players[i] != recipients[i] for i in range(len(players))):
                break

        assignments = list(zip(players, recipients))

        async with aiosqlite.connect(cls.db) as db:
            for player_id, recipient_id in assignments:
                await db.execute('''UPDATE participants SET recipient_id = ? 
                                    WHERE chat_id = ? and user_id = ?''',
                                 (str(recipient_id), str(chat_id), str(player_id)))
            await db.commit()

        return assignments

    @classmethod
    async def game_in_group(cls, group_id: int | str):
        """
        Проверяет, что игра в группе уже запущена.

        Принимает group_id --- id группы, в которой ведётся игра.

        Возвращает bool --- запущена ли игра в группе.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            async with db.execute('''SELECT 1 FROM participants
                                WHERE chat_id = ? LIMIT 1''', (group_id,)) as cursor:
                result = await cursor.fetchone()
                return result is not None

    @classmethod
    async def clear_game(cls, chat_id: int | str):
        """
        Останавливает игру в группе.

        Принимает chat_id -- id группы, в которой ведётся игра.

        Не возвращает ничего.

        Является @classmethod.
        """
        async with aiosqlite.connect(cls.db) as db:
            try:
                await db.execute(
                    "DELETE FROM participants WHERE chat_id = ?",
                    (str(chat_id),)
                )
                await db.commit()
                return True
            except:
                return False


async def update_santa_message(group_id: int | str, msg_id: int | str):
    """
    Обновляет сообщение о проведении игры "Тайный Санта" в группе.

    Принимает group_id и msg_id --- id группы, в которой ведётся игра, и id сообщения о проведении игры.

    Ничего не возвращает.
    """
    message = "Хо-хо-хо! А кто это у нас решил поиграть в тайного санту?🎅\n\nИграют:\n"
    players = await SantaGame.get_players(group_id)

    for ind, player_id in enumerate(players, 1):
        player = await bot.get_chat_member(chat_id=group_id, user_id=player_id)
        message += f"{ind}. [{player.user.first_name}](tg://user?id={player.user.id})\n"

    add_button = InlineKeyboardButton(text="Хочу быть Сантой",
                                      url=f"t.me/Mavrik_my_Bot?start={group_id[4:]}-{msg_id}-0")
    remove_button = InlineKeyboardButton(text="Передумал быть Сантой",
                                         url=f"t.me/Mavrik_my_Bot?start={group_id[4:]}-{msg_id}-1")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_button], [remove_button]])
    await bot.edit_message_text(chat_id=group_id, message_id=msg_id, text=message, parse_mode="Markdown",
                                reply_markup=keyboard)


@router.message(Command("start"))
async def start_message(msg: Message):
    """
    Обрабатывает команду /start.
    """
    args = msg.text.split()

    if len(args) > 1 and msg.chat.type == "private":
        parts = args[1].split('-')
        group_id = "-100" + parts[0]
        msg_id = parts[1]
        flag_id = parts[2]

        if flag_id == "0":
            success = await SantaGame.add_player(group_id, msg.from_user.id)

            if success:
                chat = await bot.get_chat(group_id)
                await msg.answer(f"🎄Ты присоединился к игре в чате *{chat.title}*", parse_mode="Markdown")
                await update_santa_message(group_id, msg_id)
            else:
                await msg.answer("Ты уже играешь!")
        elif flag_id == "1":
            success = await SantaGame.remove_player(group_id, msg.from_user.id)

            if success:
                chat = await bot.get_chat(group_id)
                await msg.answer(f"🎄Ты отказался от игры в чате *{chat.title}*. Если передумаешь --- возвращайся🎅",
                                 parse_mode="Markdown")
                await update_santa_message(group_id, msg_id)
            else:
                await msg.answer("Ты и так не играешь в этом чате!")
    else:
        await msg.answer("Привет! Меня зовут Маврик! Я маленький добренький котик, "
                         "живущий самой обычной жизнью) Надеюсь, мы подружимся!😸❤️\n\n"
                         "Не забудь подписаться на официальный канал -> @How_Mavrik_was_made")


@router.message(Command("santa"))
async def santa(msg: Message):
    """
    Обрабатывает команду /santa.
    """
    if msg.chat.type not in ["group", "supergroup"]:
        return await msg.answer("Я бы с радостью подарил тебе все подарки мира, "
                                "но, к сожалению, команду можно использовать "
                                "только в групповых чатах")

    chat_id = str(msg.chat.id)
    user_id = msg.from_user.id
    user = await bot.get_chat_member(chat_id, user_id)

    if user.status not in ["administrator", "creator"]:
        return await msg.answer("У тебя недостаточно прав")

    if await SantaGame.game_in_group(chat_id):
        return await msg.reply("Распределение тайных сант уже запущено!")

    add_button = InlineKeyboardButton(text="Хочу быть Сантой",
                                      url=f"t.me/Mavrik_my_Bot?start={chat_id[4:]}")
    remove_button = InlineKeyboardButton(text="Передумал быть Сантой",
                                         url=f"t.me/Mavrik_my_Bot?start={chat_id[4:]}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[add_button], [remove_button]])

    message = await msg.answer("Хо-хо-хо! А кто это у нас решил поиграть в тайного санту?🎅", reply_markup=keyboard)
    return await update_santa_message(chat_id, message.message_id)


@router.message(Command("start_santa"))
async def start_santa(msg: Message):
    """
    Обрабатывает команду /start_santa.
    """
    if msg.chat.type not in ["group", "supergroup"]:
        return await msg.answer("Эта команда не может быть запущена в личных сообщениях!")

    chat_id = str(msg.chat.id)
    user_id = msg.from_user.id
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status not in ["administrator", "creator"]:
        return await msg.answer("У тебя недостаточно прав")

    pairs = await SantaGame.make_draw(chat_id)

    if pairs is None:
        return await msg.answer("В Тайного Санту должно играть как минимум 3 человека")

    final_message = "🎁Жеребьёвка окончена! Тайными Сантами стали:\n"

    for ind, (santa_id, recipient_id) in enumerate(pairs, 1):
        santa = await bot.get_chat(santa_id)
        recipient = await bot.get_chat(recipient_id)

        await bot.send_message(chat_id=santa_id,
                               text=f"🎇Хо-хо! На этот Новый Год ты становишься тайным сантой для [{recipient.first_name}](tg://user?id={recipient_id})",
                               parse_mode="Markdown")

        final_message += f"{ind}. [{santa.first_name}](tg://user?id={santa_id})\n"

    return await msg.answer(text=final_message, parse_mode="Markdown")


@router.message(Command("clear_game"))
async def clear_game(msg: Message):
    if msg.chat.type not in ["group", "supergroup"]:
        return await msg.answer("Эта команда не может быть запущена в личных сообщениях!")

    chat_id = str(msg.chat.id)
    user_id = msg.from_user.id
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status not in ["administrator", "creator"]:
        return await msg.answer("У тебя недостаточно прав")

    success = await SantaGame.clear_game(chat_id)

    if not success:
        return await msg.answer("В этой группе не проводится игра в Тайного Санту. Но если хотите, напишите /santa")

    return await msg.answer(
        "История предыдущей игры в Тайного Санту очищена! Если хотите сыграть ещё раз, напишите /santa")

@router.message(Command("where_santa"))
async def where_santa(msg: Message):
    if msg.chat.type != "private":
        return await msg.answer("Давай не будем раскрывать твои секреты в этом чате")

    user_id = msg.from_user.id

    pairs = await SantaGame.get_player_games(user_id)

    if not pairs:
        return await msg.answer("Пока что ты не являешься Тайным Сантом ни для кого")

    final_message = "🎇Хо-хо! На этот Новый Год ты Тайный Санта для:\n"

    for ind, (chat_id, recipient_id) in enumerate(pairs, 1):
        recipient = await bot.get_chat(recipient_id)
        chat = await bot.get_chat(chat_id)
        final_message += f"{ind}. [{recipient.first_name}](tg://user?id={recipient_id}) в группе *{chat.title}*\n"

    return await msg.answer(text=final_message, parse_mode="Markdown")
