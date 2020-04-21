import csv
import re
from pprint import pprint
from pymongo import MongoClient
import json

client = MongoClient(host='192.168.66.70', port=32017)

#client.drop_database('tinder')
db = client['tinder']


def write_data(top10_with_photo):
    """
    Загрузить данные в бд
    """
    db_collection = db["people"]

    for each in top10_with_photo.values():
        temp_list = []
        for elem in each['usergroups']:
            temp_list.append(elem)
        each.update({'usergroups': temp_list})
        temp_list = []
        for elem in each['top3']:
            temp_list.append(elem)
        each.update({'top3': temp_list})

        if list(db_collection.find({'userid': each['userid']})):
            print(f"\nДубликат - {each['userid']}")
        else:
            db_collection.insert_one({
                'userid': each['userid'],
                'gender': each['gender'],
                'place': each['place'],
                'age_born': each['age_born'],
                'usergroups': each['usergroups'],
                'interests': each['interests'],
                'relation': each['relation'],
                'url': each['url'],
                'top3': each['top3']
            })
            print (f"Импортировали данные {each['userid']}")
    json_top = json.dumps(top10_with_photo)
    return json_top


def search_partner_database(source_data, right_order):
    """
    Deprecated!
    Для поиска по базе
    :return:
    """
    print("Ищем партнера по следующим данным")
    pprint(source_data)
    db_collection = db["people"]


def read_all():
    """
    Deprecated!
    """

    db_collection = db["people"]
    pprint(list(db_collection.find()))

