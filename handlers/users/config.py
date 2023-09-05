from loader import dp, bot
from aiogram import types
from api import *
from keyboards.default.buttons import *


############  Click Settings Button ###############
@dp.message_handler(text=["⚙️ Настройки", "⚙️ Sozlamalar"])
async def gotosettings(message:types.Message):
    language = language_info(message.from_user.id)
    if language == 'uz':
        await message.answer("⚙️ Sozlamalar bo'limiga xush kelibsiz!\n\n"
                             f"uz/ru  Tugmachalar orqali tilni o'zgartirishingiz mumkin.", reply_markup=settings(language))

    else:
        await message.answer("⚙️ Добро пожаловать в настройки!\n\n"
                              f"en/ru Вы можете изменить язык с помощью кнопок.", reply_markup=settings(language))


###########  Select Language  #################
@dp.message_handler(text=["uz O'zbekcha", "ru Русский"])
async def change_lang(message:types.Message):
    if message.text == "uz O'zbekcha":
        change_language(telegram_id=message.from_user.id, language="uz")
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}, @maxsus2273_bot botiga xush kelibsiz!\n\n" "Ushbu bot orqali mazali pitsalarga buyurtma bera olasiz. Pitsalar manzilingizga tezkor yetkazib beramiz!\n\n" 
                             "Buyurtna berishni boshlaysizmi?", reply_markup=main_uz)
    else:
        change_language(telegram_id=message.from_user.id, language="ru")
        await message.answer(
            f"Здравствуйте, {message.from_user.full_name}, добро пожаловать в бот @maxsus2273_bot!\n\n" "Через этого бота вы можете заказать вкусную пиццу. Доставим пиццу по вашему адресу быстро!\n\n"
             "Начать заказывать?", reply_markup=main_ru)


################  Go to Menu  ####################
@dp.message_handler(text=["Bosh menyuga qaytish", "Вернуться в главное меню"])
async def back(message:types.Message):
    language = language_info(message.from_user.id)
    if language == 'uz':
        await message.answer("✅ Bosh menyuga xush kelibsiz\n" \
                             f"🍕 Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
    else:
        await message.answer("✅ Добро пожаловать в главное меню\n" \
                             f"🍕 Вкусный пиццы! Вы начинайте заказывать?", reply_markup=main_ru)


##################  Change Language Command   #################
@dp.message_handler(commands='set_language')
async def change(message:types.Message):
    language = language_info(message.from_user.id)
    if language == 'uz':
        await message.answer("⚙️ Sozlamalar bo'limiga xush kelibsiz!\n\n"
                             f"uz/ru  Tugmachalar orqali tilni o'zgartirishingiz mumkin.",
                             reply_markup=settings(language))

    else:
        await message.answer("⚙️ Добро пожаловать в настройки!\n\n"
                             f"en/ru Вы можете изменить язык с помощью кнопок.", reply_markup=settings(language))
