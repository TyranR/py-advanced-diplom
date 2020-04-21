from pprint import pprint
import requests
import json
import time
import datetime


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


def what_are_original_user_detail(client_id):
    """
    Запрашиваем детали по искомому пользователю
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
    print('\n Можно просто нажимать ENTER.')
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
        interests = response_json['response'][0]['interests']
        interests_format = interests.split(sep=',')
    except:
        print('Интересов нет. Надо их задать')
        interests = input('Задай интересы для поиска: ')
        interests_format = interests.split(sep=',')
    try:
        pprint(response_json['response'][0]['relation'])
        relation = response_json['response'][0]['relation']
    except:
        print('Отношения не указаны')
        relation = 0
    usergroups = what_are_user_groups(client_id)
    print(f'\nГруппы будем искать такие : {usergroups}')
    final_choose = {'gender': gender, 'place': place , 'age_start': age_start, 'age_finish': age_finish, \
                   'usergroups': usergroups, 'interests': interests_format, 'relation': relation}
    # final_choose = [('gender', gender), ('place', place), ('age_start', age_start), ('age_finish', age_finish), \
    #                 ('usergroups', usergroups), ('interests', interests_format), ('relation', relation)]
    return final_choose


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
    print('\n')
    pprint(response_json)
    if response_json.get('error') and (response_json['error']['error_msg'] == 'Too many requests per second'):
        print(f"\nПридётся подождать 2 секунды, из-за ошибки {response_json['error']['error_msg'] }")
        time.sleep(2)
        response_json = response.json()
    elif response_json.get('error') and (response_json['error']['error_msg'] == 'This profile is private' or \
                                       response_json['error']['error_msg'] == 'User was deleted or banned'):
        return False
    try:
        gender = response_json['response'][0]['sex']
    except:
        gender = 0
    try:
        place = response_json['response'][0]['city']['title']
    except:
        place = ""
    try:
        age_temp = response_json['response'][0]['bdate']
        age_temp_2 = age_temp.split('.')
        age_born = int(age_temp_2[2])
    except:
        now = datetime.datetime.now()
        age_born = now.year
    try:
        pprint(response_json['response'][0]['interests'])
        interests = response_json['response'][0]['interests']
        interests_format = interests.split(sep=',')
    except:
        interests_format = []
    try:
        pprint(response_json['response'][0]['relation'])
        relation = response_json['response'][0]['relation']
    except:
        relation = 0
    usergroups = what_are_user_groups(client_id)
    url_user = 'https://vk.com/id'+str(client_id)
    client_data = {'userid': client_id, 'gender': gender, 'place': place , 'age_born': age_born, \
                   'usergroups': usergroups, 'interests': interests_format, 'relation': relation, \
                   'url': url_user}
    pprint(client_data)
    return client_data


def search_partner_dic(source_data, all_users_profiles):
    """
    Для поиска по словарю, вхождения из пользователя
    :param right_order:
    :param all_users_profiles:
    :return:
    """
    # pprint(source_data)
    match_users = {}
    count = 0
    for each in all_users_profiles.values():
        # Для точного поиска - используем полную версию требований
        # if (each['gender'] == source_data['gender'] and each['place'] == source_data['place'] and \
        #         each['age_born'] >= source_data['age_start'] and each['age_born'] <= source_data['age_start']):
        print(".", end="")
        if each['gender'] == source_data['gender']:  # для того чтобы долго не ждать, а только проверить программу
            count = count + 1
            match_users.update({each['userid']: each})

    print(f"\nСовпадений нашлось: {count}")
    return match_users


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
    # pprint(response_json)
    top3 = [{'id': 0, 'likes': 0, 'url': ""}, {'id': 0, 'likes': 0, 'url': ""}, {'id': 0, 'likes': 0, 'url': ""}]
    if response_json.get('error'):
        return top3
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
    # pprint(top3)
    return top3


def what_are_the_top_user_avatar(top):
    """
    Передаем словарь пользователей, по ним ищем фото, дописываем и возвращаем
    :return:
    """
    i = 0
    for each in top.values():
        top3 = what_are_user_avatars(each['userid'])
        each.update({'top3': {top3[0]['url'],top3[1]['url'],top3[2]['url']}})
        i = i+1
        if i == 10:
            return top
    return top


TOKEN = '40fd32ae1f5174098f69f0b910572e730386025ba7aa70a1984064eb091c1a37c07829c79f8a7fdc4610e'
url_for_token = 'https://oauth.vk.com/authorize?client_id=7401636&response_type=token&v=5.103'

