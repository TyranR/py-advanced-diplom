from pprint import pprint
from BestTinderEver.VKWorker.vkapp import *
from BestTinderEver.MongoWorker.dbwriter import *


def what_are_user_weights():
    weight_client = []
    weight_client[0] = weight_gender = int(input('Укажите вес значения пола партнера? (1-5): '))
    weight_client[1] = weight_place = int(input('Укажите вес значения места нахождения партнера? (1-5): '))
    weight_client[2] = weight_age = int(input('Укажите вес значения возраста партнера? (1-5): '))
    weight_client[3] = weight_interests = int(input('Укажите вес значения интересов партнера? (1-5): '))
    weight_client[4] = weight_relation = int(input('Укажите вес значения отношений партнера? (1-5): '))
    return weight_client


def main():
    #original_client = who_is()
    print("\nЭтап 1. Определили пользователя. Теперь определим его профиль. Press any key to continue:")
    #source_data = what_are_original_user_detail(original_client)
    print("\nЭтап 2. Определим веса для соответствия поиску. Press any key to continue:")
    # weight_client = what_are_user_weights()
    print("\nЭтап 3. Начнем искать пользователей и записывать их в базу. Press any key to continue:")
    # Наполним базу данными по порядку из вк, дубликаты пропускаем
    for i in range(1,5):
        client_data = what_are_user_detail(i)
        write_data(client_data)
    read_all()
    print("\nЭтап 4. Начнем искать соответствия по пользователям в нашей базе. Press any key to continue:")
    # Ищем по нашей базе данных пользователей по фильтру с задаными весами
    print("\nЭтап 5. Выведем ТОП10 пользователей с ТОП3 фото. Press any key to continue:")
    # what_are_user_avatars(original_client)


if __name__ == '__main__':
    main()