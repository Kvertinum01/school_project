import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from datetime import datetime, timedelta

from src.keyboards import (
    start_keyboard,
    letter_keyboard,
    help_keyboard
)
from src.variables import (
    API_TOKEN,
    ADMINS,
    WS_TYPE,
    WELCOME_MESSAGE,
    BOT_COMMANS_MESSAGE,
    UNK_CLASS_MESSAGE,
    all_letters
)
from src.schedule import (
    get_full_schedule,
    onday_schedule,
    onclass_schedule
)
from src.database import engine
from src.models import UsersTable
from src.router import Router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

router = Router()

schedule = get_full_schedule()

session = AsyncSession(engine)

waiting_save: WS_TYPE = {}

async def save_to_class(user_id: int, class_letter: str, class_num: int):
    user_inf = await session.execute(
        select(UsersTable)
        .filter(UsersTable.user_id == user_id)
    )
    user_inf: Optional[UsersTable] = user_inf.scalar()
    user_class = UsersTable(user_id, class_letter, int(class_num))
    if user_inf is None:
        session.add(user_class)
    else:
        await session.execute(
            update(UsersTable)
            .filter(UsersTable.user_id == user_id)
            .values(
                class_letter=class_letter,
                class_num=int(class_num)
            )
        )
    await session.commit()

def get_week_day(days: int = 0):
    time = datetime.today() + timedelta(days=days)
    weekday = time.weekday()
    return weekday

@router.handle("расписание")
async def schedule_today(message: Message):
    weekday = get_week_day()
    today_schedule = await onday_schedule(
        weekday, message, schedule, session
    )
    await message.answer(today_schedule)

@router.handle("расписание на завтра")
async def schedule_tomorrow(message: Message):
    weekday = get_week_day(days=1)
    tomorrow_schedule = await onday_schedule(
        weekday, message, schedule, session
    )
    await message.answer(tomorrow_schedule)

@router.handle("урок")
async def now_lesson(message: Message):
    weekday = get_week_day()
    now_time = datetime.now()
    int_time = (now_time.hour, now_time.second)
    lesson_now = await onclass_schedule(
        weekday, int_time, message, schedule, session
    )
    await message.answer(lesson_now)
    

@router.handle("следующий урок")
async def next_lesson(message: Message):
    weekday = get_week_day()
    now_time = datetime.now() + timedelta(hours=1, minutes=1)
    int_time = (now_time.hour, now_time.second)
    lesson_now = await onclass_schedule(
        weekday, int_time, message, schedule, session
    )
    await message.answer(lesson_now)

@dp.message_handler(commands=["bug"])
async def send_bug(message: Message):
    args_text = message.get_args()
    if len(args_text) < 1:
        return await message.answer(
            "Используйте команду правильно:\n/bug [найденная проблема]"
        )
    for admin in ADMINS:
        await bot.send_message(
            chat_id=admin,
            text="Получен отчет об ошибке от пользователя с id {}:\n\"{}\".".format(
                message.from_user.id, args_text
            )
        )
    await message.answer(
        "Мы получили отчёт об ошибке и постараемся исправить в близжайшее время"
    )

@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_keyboard
    )

@dp.message_handler(commands=["help", "помощь"])
async def send_help(message: Message):
    await message.answer(
        BOT_COMMANS_MESSAGE,
        parse_mode="html"
    )

@dp.message_handler(commands=["класс", "class"])
async def choose_class(message: Message):
    args_text = message.get_args()
    args = args_text.split(" ")
    if len(args) < 2:
        await message.answer(UNK_CLASS_MESSAGE)
    elif args[1] not in all_letters:
        await message.answer("Используйте только доступные буквы")
    elif (
        args[0].isdigit() \
            and not args[1].isdigit() \
                and len(args[1]) == 1
    ):
        class_letter = args[1].upper()
        class_num = args[0]
        args_text = class_num + " " + class_letter

        await save_to_class(
            message.from_user.id, class_letter, class_num
        )

        await message.answer(
            "Сохраняю вас в \"{}\" класс".format(args_text)
        )
    else:
        await message.answer(UNK_CLASS_MESSAGE)

@dp.message_handler(commands=["инфо", "info"])
async def user_info(message: Message):
    user_id = message.from_user.id
    user_inf = await session.execute(
        select(UsersTable)
        .filter(UsersTable.user_id == user_id)
    )
    user_class: Optional[UsersTable] = user_inf.scalar()
    if user_class is not None:
        class_text = str(user_class.class_num) + " " + user_class.class_letter
        await message.answer(
            "Вы сохранены в \"{}\" класс".format(class_text),
            reply_markup=help_keyboard
        )
    else:
        await message.answer("Пройдите регестрацию для сохранения в класс")

@dp.message_handler()
async def all_handler(message: Message):
    await router.check(message)

@dp.callback_query_handler(text_contains="class")
async def choose_class_num(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback = call.data.split(":")
    class_num = callback[1]

    waiting_save.update(
        {call.from_user.id: {"identify_class": class_num}}
    )

    await call.message.answer(
        "Номер класса: {}\nТеперь выберите букву".format(class_num),
        reply_markup=letter_keyboard
    )

@dp.callback_query_handler(text_contains="letter")
async def choose_class_letter(call: CallbackQuery):
    await call.answer(cache_time=60)

    callback = call.data.split(":")
    class_letter = callback[1]

    inf_dict = waiting_save.get(call.from_user.id)
    if inf_dict is not None:
        class_num = inf_dict.get("identify_class")
    else:
        return "Unknown callback"
    del waiting_save[call.from_user.id]
    rs_class = class_num + " " + class_letter

    await save_to_class(
        call.from_user.id, class_letter, class_num
    )

    await call.message.answer(
        "Сохраняю вас в \"{}\" класс".format(rs_class),
        reply_markup=help_keyboard
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)