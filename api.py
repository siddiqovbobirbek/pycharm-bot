import requests

BASE_URL = 'http://127.0.0.1.8000'

import json

def all_info(telegram_id):
    response = requests.post(f"{BASE_URL}/en/api/user/", data={
        'telegram_id': telegram_id})
    data = json.loads(response.text)
    return data


def language_info(telegram_id):
    response = requests.post(f"{BASE_URL}/en/api/user", data={
        'telegram_id': telegram_id})
    data = json.loads(response.text)
    return data['language']


def get_categories(languages):
    response = requests.get(f"{BASE_URL}/{language}/api/category/")
    data = json.loads(response.text)
    categories = [i['name'] for i in data]
    return categories


def get_all_categories():
    response = requests.get(f"{BASE_URL}/en/api/category")
    data = json.loads(response.text)
    category_uz = [i['name_uz'] for i in data]
    category_ru = [i['name_ru'] for i in data]
    return category_uz+category_ru


def category_info(language, category):
    response = requests.get(f"{BASE_URL}/{language}/api/category/?search={category}")
    data = json.loads(response.text)
    data = data[0]
    if data['subcategory'] == []:
        categories = []
        for i in data['products']:
            data = {}
            data['id'] = i['id']
            data['name'] = i['name']
            data['price'] = i['price']
            data['image'] = i['image']
            categories.append(data)
        info = {'products': categories}
    else:
        categories = [i['name'] for i in data['subcategory']]
        info = {'subcategory': categories}

    return info


def subcategory_info(language, subcategory):
    response = requests.get(f"{BASE_URL}/{language}/api/subcategory/?search={subcategory}")
    data = json.loads(response.text)
    return data[0]['products']

def get_product(id, language):
    response = requests.get(f"{BASE_URL}/{language}/api/product/{id}")
    data = json.loads(response.text)
    return data

def create(name, telegram_id):
    response = requests.post(f"{BASE_URL}/en/api/botuser/", data={"name": name, "telegram_id": telegram_id})
    return response.status_code

def change_language(telegram_id, language):
    response = requests.post(f"{BASE_URL}/en/api/change/", data = {'telegram_id': telegram_id, 'language':language})
    return response.status_code

def change_phone(telegram_id, phone):
    response = requests.post(f"{BASE_URL}/en/api/phone/", data={'telegram_id': telegram_id, 'phone': phone})
    return response.status_code

def shop_info(telegram_id, language):
    response = requests.post(f'{BASE_URL}/{language}/api/shop/', data={'telegram_id': telegram_id})
    data = json.loads(response.text)
    return data

def set_order(telegram_id, product, quantity):
    response = requests.post(f'{BASE_URL}/en/api/set_order/',
                             data={'telegram_id': telegram_id, 'product': product, 'quantity': quantity})
    data =json.loads(response.text)
    return data


def delete_basket(telegram_id):
    response = requests.post(f'{BASE_URL}/en/api/delete_basket/', data = {'telegram_id': telegram_id})
    data = json.loads.(response.text)
    return data

def delete_item(telegram_id, product):
    response = request.post(f'{BASE_URL}/en/api/delete_item/', data = {'telegram_id': telegram_id, 'product': product})
    data = json.loads(response.text)
    return data