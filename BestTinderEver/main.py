from pprint import pprint
from BestTinderEver.VKWorker.vkapp import *
from BestTinderEver.MongoWorker.dbwriter import *
from operator import itemgetter

# def what_are_user_weights(source_data):
#     """
#     Deprecated!
#     :param source_data:
#     :return:
#     """
#     # gender = int(input('Укажите вес значения пола партнера? (1-5): '))
#     # place = int(input('Укажите вес значения места нахождения партнера? (1-5): '))
#     # age = int(input('Укажите вес значения пола партнера? (1-5): '))
#     # interest = int(input('Укажите вес значения интересов партнера? (1-5): '))
#     # relation = int(input('Укажите вес значения отношений партнера? (1-5): '))
#     gender = 5
#     place = 4
#     age = 3
#     interest = 2
#     relation = 1
#     final_choose = [('gender', source_data[0][1], gender), ('place', source_data[1][1], place), ('age_start', \
#                     source_data[2][1], age), ('age_finish', source_data[3][1], age), ('usergroups', source_data[4][1], \
#                     0), ('interests', source_data[5][1], interest), ('relation', source_data[6][1], relation)]
#     right_order = sorted(final_choose, key=itemgetter(2), reverse=True)
#     return right_order

def main():
    original_client = who_is()
    print("\nЭтап 1. Определили пользователя. Теперь определим его профиль и дополним недостающими параметрами.")
    source_data = what_are_original_user_detail(original_client)
    # print("\nЭтап 2. Определим веса для соответствия поиску. Press any key to continue:")
    #Необязательно, если ищем не по базе, а из словаря all_users_profiles
    #right_order = what_are_user_weights(source_data)
    print("\nЭтап 2. Начнем искать пользователей и получать данные из профиля.")
    # Наполним базу данными по порядку из вк
    all_users_profiles = {}
    for i in range(20,100):
        client_data = what_are_user_detail(i)
        if client_data:
            all_users_profiles.update({i: client_data}) # добавляем в словарь пользователя (если он существует)
    print("\nЭтап 3. Начнем искать соответствия по пользователям с по заданным критериям.")
    # Ищем парнтеров сравнивая с требованиями пользователя по всем профилям из тех что нашли ранее
    match_people = search_partner_dic(source_data, all_users_profiles)
    print("\nЭтап 4. Выведем ТОП10 пользователей с ТОП3 фото. ")
    # Передаем список c найденными партнерами, ищем у них аватары, дописываем в пользователей и
    # первые 10 штук возврашаем
    top10_with_photo = what_are_the_top_user_avatar(match_people)
    print("\nЭтап 5. Записываем полученных пользователей в базу данных.")
    json_finish = write_data(top10_with_photo)  # записываем базу получаем финальный JSON
    pprint(json_finish)


if __name__ == '__main__':
    main()