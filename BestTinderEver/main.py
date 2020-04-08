from pprint import pprint
import requests
import json
import time
from urllib.parse import urlencode
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
            print("Будет использован пользователь по умолчанию, 171691064/eshmargunov")
            return 171691064
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


def main():
    original_client = who_is()
    print("\nЭтап 1. Определили пользователя. Теперь определим его группы. Press any key to continue:")


TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

if __name__ == '__main__':
    main()