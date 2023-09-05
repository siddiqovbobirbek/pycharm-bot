from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.default.buttons import *
from api import *
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils import callback_data

@dp.message_handler(text=["Otmetit", "Bekor qilish"])
async def cancelfunction(message: types.Message):
    language = language_info(message.from_user.id)
    if language == "uz":
        await message.answer("Bosh menyuga xush kelibsiz!\n" \
                             f"Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
    else:
        await message.answer("Добро пожаловать в главное меню!\n" \
                             f"Вкусные пиццы! Начать заказывать?", reply_markup=main_ru)


@dp.message_handler(Text(startswith='Bir daqiqa ...'))
async def subcategory_product(message: types.Message, state: FSMContext):
    await message.answer("Ok")
    await state.update_data({
        "level": "subcategory"
    })
    language = language_info(message.from_user.id)
    key = message.text[1:]
    datas = subcategory_info(language=language, subcategory=key)
    data = datas[0]
    money = "so'm" if language == 'uz' else "сум"
    sena = "Narxi" if language == 'uz' else "Цена"
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.row(KeyboardButton(text="Orqaga"), KeyboardButton(text="Savat"))
    if language == 'ru':
        button.row(KeyboardButton(text="Назад"), KeyboardButton(text="Корзина"))
    await message.answer("Pastga", reply_markup=button)
    await message.answer_photo(photo=data['image'], caption=f"<b>{data['name']}</b>\n\n{sena}: {data['price']} {money}",
                               reply_markup=product_button(data=datas, language=language))


@dp.message_handler(Text(startswith="Chapga"))
async def test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data.get('level', None)
    language = language_info(message.from_user.id)
    if level == 'subcategory':
        if language == 'uz':
            await message.answer("⬇️ Kategoriyani tanglang", reply_markup=categories(language))
        else:
            await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))

    if level == "category":
        if language == "uz":
            await message.answer("Bosh menyuga xush kelibsiz!\n" \
                                 f"Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
        else:
            await message.answer("Добро пожаловать в главное меню!\n" \
                                 f"Вкусные пиццы! Начать заказывать?", reply_markup=main_ru)

    elif level == 'product-category':
        await state.update_data({
            "level": "category"
        })
        if language == 'uz':
            await message.answer("⬇️ Kategoriyani tanglang", reply_markup=categories(language))
        else:
            await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))

    else:
        if language == "uz":
            await message.answer("Bosh menyuga xush kelibsiz!\n" \
                                 f"Mazali pitsalar! Buyurtma berishni boshlaysizmi?", reply_markup=main_uz)
        else:
            await message.answer("Добро пожаловать в главное меню!\n" \
                                 f"Вкусные пиццы! Начать заказывать?", reply_markup=main_ru)


########### Go to Menus ###################
@dp.message_handler(text=["Меню", "Menyu"])
async def category(message: types.Message, state: FSMContext):
    await state.update_data({
        "level": "category"
    })
    telegram_id = message.from_user.id
    language = language_info(telegram_id=telegram_id)
    if language == 'uz':
        await message.answer("⬇️ Kategoriyani tanglang", reply_markup=categories(language))
    else:
        await message.answer("⬇️ Выберите категорию", reply_markup=categories(language))


############ Go to Categories product or Subcategory  ##############
@dp.message_handler(text=get_all_categories())
async def test(message: types.Message, state: FSMContext):
    language = language_info(message.from_user.id)
    category = category_info(language=language, category=message.text)
    if 'subcategory' in category:
        await message.answer("⬇️", reply_markup=product_or_subcategory(category=message.text, language=language))
    else:
        await state.update_data({
            "level": "product-category"
        })
        data = category['products'][0]
        money = "so'm" if language == 'uz' else "сум"
        sena = "Narxi" if language == 'uz' else "Цена"
        button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if language == 'uz':
            button.row(KeyboardButton(text="Orqaga"), KeyboardButton(text="Savat"))
        if language == 'ru':
            button.row(KeyboardButton(text="Назад"), KeyboardButton(text="Корзина"))
        await message.answer("Pastga", reply_markup=button)
        await message.answer_photo(photo=data['image'],
                                   caption=f"<b>{data['name']}</b>\n\n{sena} : {data['price']} {money}",
                                   reply_markub=product_or_subcategory(category=message.text, language=language,
                                                                       product=data['id']))


############  Show Product  (Inline Button)  #############

@dp.callback_query_handler(callback.filter())
async def decrease(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = callback_data
    language = language_info(call.from_user.id)
    if data['action'] == 'next':
        money = "so'm" if language == 'uz' else "сум"
        sena = "Narxi" if language == 'uz' else "Цена"
        product = get_product(language=language, id=data['product'])
        await call.message.edit_media(media=InputMediaPhoto(media=product['image'],
                                                            caption=f"<b>{product['name']}</b>\n\n" f"{sena}: {product['price']} {money}"),
                                      reply_markup=to_product(language=language, product=product['id'], count=1))

    if data['action'] == 'increase':
        if language == 'uz':
            await call.answer(f"{int(data['count']) + 1} ta")
            count = int(data['count']) + 1
            await call.message.edit_reply_markup(
                reply_markup=to_product(language=language, product=int(data['product']), count=count))
        else:
            await call.answer(f"{int(data['count']) + 1} шт")
            count = int(data['count']) + 1
            await call.message.edit_reply_markup(
                reply_markup=to_product(language=language, product=int(data['product']), count=count))

    if data['action'] == 'decrease':
        if language == 'uz':
            if int(data['count']) == 1:
                await call.answer(f"{int(data['count'])} ta")
                count = int(data['count'])
                await call.message.edit_reply_markup(
                    reply_markup=to_product(language=language, product=int(data['product']), count=count))
            await call.answer(f"{int(data['count']) - 1} ta")
            count = int(data['count']) - 1
            await call.message.edit_reply_markup(
                reply_markup=to_product(language=language, product=int(data['product']), count=count))
        else:
            if int(data['count']) == 1:
                await call.answer(f"{int(data['count'])} шт")
                count = int(data['count'])
                await call.message.edit_reply_markup(
                    reply_markup=to_product(language=language, product=int(data['product']), count=count))
            await call.answer(f"{int(data['count']) - 1} шт")
            count = int(data['count']) - 1
            await call.message.edit_reply_markup(
                reply_markup=to_product(language=language, product=int(data['product']), count=count))

    if data['action'] == 'add':
        telegram_id = call.from_user.id
        quantity = int(data['count'])
        product = int(data['product'])
        await call.message.delete()
        set_order(telegram_id=telegram_id, product=product, quantity=quantity)
        await state.update_data({
            'level': 'category'
        })
        if language == 'uz':
            await call.message.answer("<i>Mahsulot savatingizga qo'shildi.</i>")
            await call.message.answer("⬇️ Kategoriyani tanlang", reply_markup=categories(language))
        else:
            await call.message.answer("<i>Товар добавлен в корзину.</i>")
            await call.message.answer("⬇️ Выберите категорию", reply_markup=categories(language))
