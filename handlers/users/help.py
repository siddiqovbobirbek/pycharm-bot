from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Qanday yordam kerak? / Какая помощь нужна?",
            "Buyruqlar: / Команды: ",
            "/start - Botni ishga tushirish / Запустить бота",
            "/help - Yordam / Помощь")
    
    await message.answer("\n".join(text))
