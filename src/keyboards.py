from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="6", callback_data="class:6"),
            InlineKeyboardButton(text="7", callback_data="class:7"),
            InlineKeyboardButton(text="8", callback_data="class:8")
        ],
        [
            InlineKeyboardButton(text="9", callback_data="class:9"),
            InlineKeyboardButton(text="10", callback_data="class:10"),
            InlineKeyboardButton(text="11", callback_data="class:11"),
        ]
    ]
)

letter_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="И", callback_data="letter:И")
        ]
    ]
)