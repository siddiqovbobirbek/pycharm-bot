from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.callback_data import CallbackData

callback = CallbackData("action", "product", "count", "language")

from api import *


basket_callback = CallbackData('mykb', 'action', 'product')
callback = CallbackData('ikb', 'action', 'count', 'product')
choose_language = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
choose_language.insert(KeyboardButton('🇺🇿 O\'zbekcha')).insert(KeyboardButton('🇷🇺 Русский'))
main_uz = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_uz.insert(KeyboardButton(text="📝 Menu")).row(KeyboardButton(text="📖 Buyurtmalarim"),
                                                  KeyboardButton(text="📥 Savat"), KeyboardButton(text="⚙️ Sozlamalar"),
                                                  KeyboardButton(text="✍️ Sharh qoldiring"))
main_ru = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_ru.insert(KeyboardButton(text="📝 Меню")).row(KeyboardButton(text="📖 Мои заказы"), KeyboardButton(text="📥 Корзина"),
                                                  KeyboardButton(text="⚙️ Настройки"),
                                                  KeyboardButton(text="✍️ Оставить отзыв"))


def categories(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="📥 Savat"))
    else:
        button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="📥 Корзина"))
    categories = get_categories(language)
    for i in categories:
        button.insert(KeyboardButton(text=i))

    return button


def product_or_subcategory(category, language, product=None):
    data = category_info(language=language, category=category)
    if 'subcategory' in data:
        button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if language == 'uz':
            button.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=callback.new(action='back',  language=language)))
            button.row(InlineKeyboardButton(text="📥 Savat", callback_data=callback.new(action='basket', language=language)))
        else:
            button.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=callback.new(action='back', language=language)))
            button.row(InlineKeyboardButton(text="📥 Корзина", callback_data=callback.new(action='basket', language=language)))
        datas = data['subcategory']
        for data in datas:
            button.insert(KeyboardButton(text= f" {data}"))
        return button
    else:
        button = InlineKeyboardMarkup()
        data = data['products']
        if len(data) > 1:
            for i in data[1:]:
                button.add(InlineKeyboardButton(text=f"{i['name']} - {i['price']}", callback_data=callback.new(action='add', product=i['id'], language=language)))
        button.row(
            InlineKeyboardButton(text="-", callback_data=callback.new(action='decrease', product=str(data[0]['id']))),
            InlineKeyboardButton(text="1", callback_data="1"),  # You can adjust this part as needed
            InlineKeyboardButton(text="+", callback_data=callback.new(action='increase', product=data['id']))
        )

        if language == 'ru':
            button.add(InlineKeyboardButton(text="📥 Добавить в корзину",
                                            callback_data=callback.new(action='add', product=data['id'], language=language)))
        else:
            button.add(InlineKeyboardButton(text="📥 Savatga qo'shish",
                                            callback_data=callback.new(action='add', product=data['id'], language=language)))
        return button


############# Product #############
def to_product(language, product, count):
    button = InlineKeyboardMarkup()
    button.row(
        InlineKeyboardButton(text="-",  callback_data=callback.new(action='decrease')),
        InlineKeyboardButton(text=f"{product['count']}", callback_data=product['count']),
        InlineKeyboardButton(text="+", callback_data=callback.new(action='increase'))
    )
    if language == 'ru':
        button.add(InlineKeyboardButton(text="📥 Добавить в корзину",
                                        callback_data=basket_callback.new(action='add', product=product)))
    else:
        button.add(InlineKeyboardButton(text="📥 Savatga qo'shish",
                                        callback_data=basket_callback.new(action='add', product=product)))

    return button


############## Button Settings
def settings(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button.row(InlineKeyboardButton(text="🇺🇿 O'zbekcha"), InlineKeyboardButton(text="🇷🇺 Русский"))
    if language == 'ru':
        # return to main menu
        button.row(InlineKeyboardButton(text="🔝 Вернуться в главное меню", ))
    else:
        button.row(InlineKeyboardButton(text="🔝 Bosh menyuga qaytish", ))

    return button


############## Button Comment ##############
def cancel(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'ru':
        # cancel
        button.row(InlineKeyboardButton(text="❌ Отменить", ))
    else:
        button.row(InlineKeyboardButton(text="❌ Bekor qilish", ))

    return button


############## Button Basket ##############
def mybasket(language, datas):
    button = InlineKeyboardMarkup()
    if language == 'ru':
        # cancel
        button.row(
            InlineKeyboardButton(text="🗑 Очистить корзину", callback_data=basket_callback.new(action='clear', product=0)),
            InlineKeyboardButton(text="🚖 Оформить заказ", callback_data=basket_callback.new(action='order', product=0))
        )
    else:
        button.row(
            InlineKeyboardButton(text="🗑 Savatni tozalash",
                                 callback_data=basket_callback.new(action='clear', product=0)),
            InlineKeyboardButton(text="🚖 Buyurtma berish", callback_data=basket_callback.new(action='order', product=0))
        )

    for data in datas:
        button.add(InlineKeyboardButton(text=f"❌ {data['product']}",
                                        callback_data=basket_callback.new(action='delete', product=data['product'])))

    return button


############## Get Contact ##############
def getcontact(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.add(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    else:
        button.add(KeyboardButton(text="📞 Отправить номер телефона", request_contact=True))
        button.row(KeyboardButton(text="❌ Отменить"))

    return button


############## Product Button ##############
def product_button(data, language):
    button = InlineKeyboardMarkup()
    product = data[0]['product']
    if len(data) > 1:
        for i in data[1:]:
            button.add(InlineKeyboardButton(text=f"{i['name']} - {i['price']}",
                                            callback_data=basket_callback.new(action='next', product=i['id'])))
    button.row(
        InlineKeyboardButton(text=f"-", callback_data=callback.new(action='decrease')),
        InlineKeyboardButton(text=f"{product['count']}", callback_data=product['count']),
        InlineKeyboardButton(text=f"+", callback_data=callback.new(action='increase'))
    )

    if language == 'ru':
        button.add(InlineKeyboardButton(text="📥 Добавить в корзину",
                                        callback_data=basket_callback.new(action='add', count=1,
                                                                          product=product['id'])))
    else:
        button.add(InlineKeyboardButton(text="📥 Savatga qo'shish",
                                        callback_data=basket_callback.new(action='add', count=1,
                                                                          product=product['id'])))

    return button


############## Payment ##############
def payment(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.add("💸 Naqd")
        button.add("🟦 Click")
        button.add("🟩 Payme")
        button.row(KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="❌ Bekor qilish"))
    else:
        button.add("💸 Наличные")
        button.add("🟦 Click")
        button.add("🟩 Payme")
        button.row(KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отменить"))

    return button


############## Get Address ##############
def mylocation(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.add(KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    else:
        button.add(KeyboardButton(text="📍 Отправить местоположение", request_location=True))
        button.row(KeyboardButton(text="❌ Отменить"))


############## Type of Getting Product ##############
def gettype(language):
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if language == 'uz':
        button.add(KeyboardButton(text="🏃‍♂️ Olib ketish"))
        button.add(KeyboardButton(text="🚕 Yetkazish"))
        button.row(KeyboardButton(text="❌ Bekor qilish"))
    else:
        button.add(KeyboardButton(text="🏃‍♂️ Самовывоз"))
        button.add(KeyboardButton(text="🚕 Доставка"))
        button.row(KeyboardButton(text="❌ Отменить"))

    return button

