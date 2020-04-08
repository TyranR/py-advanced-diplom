import csv
import re
from pprint import pprint
from pymongo import MongoClient

client = MongoClient(host='192.168.66.74', port=32017)

def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    client.drop_database(db)
    db = client[db]
    db_collection = db["artists"]
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            db_collection.insert_one({
                'Исполнитель': row["Исполнитель"],
                'Цена': int(row["Цена"]),
                'Место': row["Место"],
                'Дата': row["Дата"]
            })
            # print(row["Исполнитель"], row["Цена"], row["Место"], row["Дата"])
    # pprint(list(db_collection.find()))
    return "Импортировали данные"

