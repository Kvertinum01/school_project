import dotenv
import os
from typing import Dict, Union

dotenv.load_dotenv()

API_TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DB_URL")

WELCOME_MESSAGE = (
    "Для дальнейшего использования бота выберите класс,\n"
    "нажав на одну из кнопок или используйте команду\n"
    "/класс [НОМЕР] [БУКВА]"
)

UNK_CLASS_MESSAGE = (
    "Используйте команду правильно:\n"
    "/класс [НОМЕР] [БУКВА]"
)

BOT_COMMANS_MESSAGE = (
    "Все существующие команды на данный момент:\n"
    "/help <i>Показывает текущий текст</i>\n"
    "/class <i>Сохраняет вас в класс</i>\n"
    "/info <i>Показывает, в каком классе вы сохранены</i>\n"
)

WS_TYPE = Dict[int, Dict[str, Union[str, int]]]
