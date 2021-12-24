from openpyxl import load_workbook

from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from typing import Optional

from .models import UsersTable

wb = load_workbook('./schedule.xlsx')

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

async def onday_schedule(
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
    class_name =  str(user_inf.class_num) + user_inf.class_letter.lower()
    class_schedule: dict = schedule_day[class_name]
    lessons_text = ""
    for lesson_num, lesson_str in class_schedule.items():
        lessons_text += "{} - {}\n".format(lesson_num, lesson_str)
    return (
        "Расписание на день недели {}:\n{}".format(strday, lessons_text)
    )