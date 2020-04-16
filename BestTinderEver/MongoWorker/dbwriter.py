import csv
import re
from pprint import pprint
from pymongo import MongoClient

client = MongoClient(host='192.168.66.73', port=32017)

# client.drop_database('tinder')
db = client['tinder']

def write_data(client_data):
    """
    Загрузить данные в бд
    """
    db_collection = db["people"]
    if list(db_collection.find({'userid': client_data['userid']})):
        pass
    else:
        db_collection.insert_one({
            'userid': client_data['userid'],
            'gender': client_data['gender'],
            'place': client_data['place'],
            'age_born': client_data['age_born'],
            'usergroups': client_data['usergroups'],
            'interests': client_data['interests'],
            'relation': client_data['relation'],
            'url': client_data['url']
        })
        print (f"Импортировали данные {client_data['userid']}")
    return True

def read_all():
    db_collection = db["people"]
    pprint(list(db_collection.find()))

