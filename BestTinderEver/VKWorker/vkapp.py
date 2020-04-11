from pprint import pprint
import requests
import json
import time
import datetime
from BestTinderEver.MongoWorker.dbwriter import read_data as mongoworker


def who_is():
    """
    Задаем пользователя для работы
    """
    client_id = input("Введите имя пользователя или его ID: ")
    try:
        int(client_id)
        print(f"Будет использован пользователь {client_id}")
        return int(client_id)
    except ValueError:
        if client_id == "":
            #print("Будет использован пользователь по умолчанию, 171691064/eshmargunov")
            #return 171691064
            print("Будет использован пользователь по умолчанию, 288925483/ruslankarmanov")
            return 288925483
        else:
            print(f"Будет использован пользователь {client_id}")
            user_id = if_user_id_is_not_int(client_id)
            return int(user_id)


def if_user_id_is_not_int(client_id):
    """
    Если пользователь введен не по ID, то получаем его ID
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_ids': client_id,
    }
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params
    )
    response_json = response.json()
    user_id = response_json['response'][0]['id']

    print(f"Печатаем результат превращения - {user_id}")
    return int(user_id)


def what_are_user_groups(client_id):
    """
    Запрашиваем группы у пользователя
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id,
        'extended': 1,
        'count': 1000
    }
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params
    )
    response_json = response.json()
    usergroups = set()
    if response_json.get('error') and (response_json['error']['error_msg'] == 'This profile is private' or \
                                       response_json['error']['error_msg'] == 'User was deleted or banned'):
        print(f"\nНе можем посмотреть группы у друга {client_id} "
              f"из-за ошибки {response_json['error']['error_msg']}")
        return usergroups
    elif response_json.get('error') and (response_json['error']['error_msg'] == 'Too many requests per second'):
        print(f"\nПридётся подождать 1 секунду, из-за ошибки {response_json['error']['error_msg'] }")
        time.sleep(1)
        response_json = response.json()
    print(f"\nИщем группы у пользователя {client_id}: ")
    try:
        for group in response_json['response']['items']:
            print(".", end="")
            usergroups.add(group['id'])
        return usergroups
    except:
        return usergroups


def what_are_user_detail(client_id):
    """
    Запрашиваем детали по пользователю
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id,
        'extended': 1,
        'count': 1000,
        'fields': 'sex,city,bdate,interests,relation'
    }
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params
    )
    response_json = response.json()
    pprint(response_json)
    try:
        if response_json['response'][0]['sex'] == 2:
            answer = input('Ищем женщину? (y/n): ')
            if answer == ('y' or ''):
                gender = 1
            else:
                gender = 2
        else:
            answer = input('Ищем мужчину? (y/n): ')
            if answer == ('y' or ''):
                gender = 2
            else:
                gender = 1
    except:
        answer = input('Ищем женщину или мужчину? (f/m): ')
        if answer == ('f' or ''):
            gender = 2
        else:
            gender = 1
    try:
        place = response_json['response'][0]['city']['title']
        answer = input(f'Ищём в {place}? (y/n): ')
        if answer == 'n':
            place = input('Введи город для поиска: ')
    except:
        answer = input(f'Ищём в Москве? (y/n): ')
        if answer == 'n':
            place = input('Введи город для поиска: ')
        else:
            place = 'Москва'
    now = datetime.datetime.now()
    try:
        age_temp = response_json['response'][0]['bdate']
        age_temp_2 = age_temp.split('.')
        age_year = int(age_temp_2[2])
        age = now.year - age_year
    except:
        age = 21
    age_client = now.year-age
    age_start = age_finish = age_client
    answer = input(f'Ищем - {age}-летних? (y/n): ')
    if answer == 'n':
        answer = input('Введи диапазон возраста (40-45): ')
        answer_temp = answer.split('-')
        age_start = now.year - int(answer_temp[0])
        age_finish = now.year - int(answer_temp[1])
    print(f'Будем искать родившихся с {age_finish} до {age_start}')
    try:
        pprint(response_json['response'][0]['interests'])
    except:
        print('Интересов нет')
    try:
        pprint(response_json['response'][0]['relation'])
    except:
        print('Отношения не указаны')


def what_are_user_avatars(client_id):
    """
    Топ 3 Фотографий аватара пользователя
    :param client_id:
    :return:
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id,
        'extended': 1,
        'count': 1000,
        'album_id': 'profile'
    }
    response = requests.get(
        'https://api.vk.com/method/photos.get',
        params
    )
    response_json = response.json()
    pprint(response_json['response']['items'])
    top3 = [{'id': 0, 'likes': 0, 'url': ""}, {'id': 0, 'likes': 0, 'url': ""}, {'id': 0, 'likes': 0, 'url': ""}]
    for each in response_json['response']['items']:
        if each['likes']['count'] > top3[0]['likes']:
            top3[2]['id'] = top3[1]['id']
            top3[2]['likes'] = top3[1]['likes']
            top3[2]['url'] = top3[1]['url']
            top3[1]['id'] = top3[0]['id']
            top3[1]['likes'] = top3[0]['likes']
            top3[1]['url'] = top3[0]['url']
            top3[0]['id'] = each['id']
            top3[0]['likes'] = each['likes']['count']
            top3[0]['url'] = each['sizes'][0]['url']
        elif each['likes']['count'] > top3[1]['likes']:
            top3[2]['id'] = top3[1]['id']
            top3[2]['likes'] = top3[1]['likes']
            top3[2]['url'] = top3[1]['url']
            top3[1]['id'] = each['id']
            top3[1]['likes'] = each['likes']['count']
            top3[1]['url'] = each['sizes'][0]['url']
        elif each['likes']['count'] > top3[2]['likes']:
            top3[2]['id'] = each['id']
            top3[2]['likes'] = each['likes']['count']
            top3[2]['url'] = each['sizes'][0]['url']
    pprint(top3)
    return top3


TOKEN = '54388f42ee9169ad76080cfc55b60af344884ddf36ac1721674a218962da0d979d06b1ed2d25f875fb028'

