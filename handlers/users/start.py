from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp
from api import *
from keyboards.default.buttons import *
from states.languages import Language


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")

    full_name = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id
    check = create(username, telegram_id, full_name)
    if check == 400:
        language = language_info(telegram_id)
        if language == 'uz':
            await message.answer("✅ Bosh menyuga xush kelibsiz\n"\
            f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
        elif language == 'ru':
            await message.answer("✅ Добро пожаловать в главное меню\n"\
            f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)
    else:
        await message.answer(f"🇺🇿 Botdan foydalanish uchun o'zingizga qulay tilni tanlang.\n"\
                            f"🇷🇺 Для использования бота выберите удобный для вас язык.\n"\
                            f"🇬🇧 Choose a convenient language for you to use the bot.",
                            reply_markup=choose_language)
        create(username, telegram_id, full_name)
        await Language.language.set()

@dp.message_handler(state=Language.language)
async def set_language_system(message: types.Message, state:FSMContext):
    if message.content_type == 'text':
        if message.text in ['🇺🇿 O\'zbekcha', '🇷🇺 Русский']:
            if message.text == '🇺🇿 O\'zbekcha':
                change_language(telegram_id=message.from_user.id, language='uz')
                await message.answer("✅ Bosh menyuga xush kelibsiz\n"\
                f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
            elif message.text == '🇷🇺 Русский':
                change_language(telegram_id=message.from_user.id, language='ru')
                await message.answer("✅ Добро пожаловать в главное меню\n"\
                f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)
            await state.finish()
        else:
            await message.answer(" 🇺🇿 Botdan foydalanish uchun o'zingizga qulay tilni tanlang.\n"\
                                 " 🇷🇺 Для использования бота выберите удобный для вас язык.\n"\
                                    " 🇬🇧 Choose a convenient language for you to use the bot.",
                                    reply_markup=choose_language)
            await Language.language.set()
    else:
        await message.answer(" 🇺🇿 Botdan foydalanish uchun o'zingizga qulay tilni tanlang.\n"\
                                    " 🇷🇺 Для использования бота выберите удобный для вас язык.\n"\
                                        " 🇬🇧 Choose a convenient language for you to use the bot.",
                                        reply_markup=choose_language)
        await Language.language.set()