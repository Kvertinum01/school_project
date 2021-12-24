from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="6", callback_data="class:6"),
            InlineKeyboardButton(text="7", callback_data="class:7")
        ],
        [
            InlineKeyboardButton(text="8", callback_data="class:8"),
            InlineKeyboardButton(text="9", callback_data="class:9")
        ]
    ]
)

letter_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="И", callback_data="letter:И"),
            InlineKeyboardButton(text="Е", callback_data="letter:Е"),
            InlineKeyboardButton(text="З", callback_data="letter:З"),
            InlineKeyboardButton(text="Г", callback_data="letter:Г")
        ],
        [
            InlineKeyboardButton(text="К", callback_data="letter:К"),
            InlineKeyboardButton(text="С", callback_data="letter:С"),
            InlineKeyboardButton(text="Т", callback_data="letter:Т"),
            InlineKeyboardButton(text="Ж", callback_data="letter:Ж")
        ]
    ]
)

help_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Расписание")
        ],
        [
            KeyboardButton(text="Расписание на завтра")
        ]
    ],
    resize_keyboard=True
)