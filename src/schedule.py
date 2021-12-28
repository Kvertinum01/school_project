from openpyxl import load_workbook

from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from typing import Optional

from .models import UsersTable

wb = load_workbook('./schedule.xlsx')

lessons = [(8+i)+0.5 for i in range(9)]

clases = ["C", "E", "G", "I", "K", "M", "O", "Q"]
days = ["понедельник", "вторник", "среда", "четверг", "пятница"]
class_row = 9

def get_schedule(day):
    sheet = wb[day]
    classes_inf = {}

    for class_ind in range(4):
        for now_class in clases:
            number = 2+class_row*class_ind
            letter = now_class + str(number)
            cell = sheet[letter]
            if cell.value is None:
                continue
            name = cell.value
            if "(" in name:
                name = name[0] + name[3]
            classes_inf.update(
                {
                    name: {
                        "letter": now_class,
                        "number": number,
                        "pos": cell.coordinate
                    }
                },
            )

    schedule = {}

    for class_fullletter in classes_inf:
        now_dict = {class_fullletter: {}}
        class_inf_now = classes_inf[class_fullletter]
        letter = class_inf_now["letter"]
        for num in range(8):
            number = class_inf_now["number"] + (num+1)
            cell = sheet[letter+str(number)]
            if cell.value is None or cell.value == "-":
                continue
            now_dict[class_fullletter].update(
                {str(num+1): cell.value}
            )
        schedule.update(now_dict)

    return schedule

def get_full_schedule():
    full_schedule = {}
    for day in days:
        schedule = get_schedule(day)
        full_schedule.update(
            {day: schedule}
        )
    return full_schedule

async def schedule_dict(
    day: int,
    message: Message,
    schedule: dict,
    session: AsyncSession
):
    if day in (5, 6):
        return "На выходных нет уроков"
    strday = days[day]
    schedule_day = schedule[strday]
    user_id = message.from_user.id
    user_inf = await session.execute(
        select(UsersTable)
        .filter(UsersTable.user_id == user_id)
    )
    user_inf: Optional[UsersTable] = user_inf.scalar()
    if user_inf is None:
        return "Пройдите регестрацию для сохранения в класс"
    class_name =  str(user_inf.class_num) + user_inf.class_letter.lower()
    if class_name not in schedule_day:
        return "Ваш класс не найден, пройдите регестрацию повторно, используя команду /start"
    class_schedule: dict = schedule_day[class_name]
    return class_schedule

async def onday_schedule(
    day: int,
    message: Message,
    schedule: dict,
    session: AsyncSession
):
    strday = days[day]
    class_schedule = await schedule_dict(
        day, message, schedule, session
    )
    if not isinstance(class_schedule, dict):
        return class_schedule
    lessons_text = ""
    for lesson_num, lesson_str in class_schedule.items():
        lessons_text += "{} - {}\n".format(lesson_num, lesson_str)
    return (
        "Расписание на день недели {}:\n{}".format(strday, lessons_text)
    )

def dict_index(wdict: dict, ind: int):
    wlist = list(wdict.keys())
    element = wlist[ind]
    return wdict[element]

async def onclass_schedule(
    day: int,
    time: tuple,
    message: Message,
    schedule: dict,
    session: AsyncSession
):
    minutes = time[1]/60
    if 15 < time[1] <= 29:
        minutes = 0.5
    curtime = time[0] + minutes
    if curtime > lessons[-2]:
        day += 1
        time = (8, 30)
    class_schedule = await schedule_dict(
        day, message, schedule, session
    )
    if not isinstance(class_schedule, dict):
        return class_schedule
    now_lesson = 0
    for ntime in lessons:
        if ntime <= curtime+0.25 <= ntime+1:
            now_lesson = int(ntime - 8.5)
            break
    str_lesson = dict_index(class_schedule, now_lesson)
    return "{} урок - {}.".format(now_lesson+1, str_lesson)
    