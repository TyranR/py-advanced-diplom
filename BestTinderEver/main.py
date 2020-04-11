from pprint import pprint
from BestTinderEver.VKWorker.vkapp import *


def what_are_user_weights():
    weight_client = []
    weight_client[0] = weight_gender = input('Укажите вес значения пола партнера? (1-5): ')
    weight_client[1] = weight_place = input('Укажите вес значения места нахождения партнера? (1-5): ')
    weight_client[2] = weight_age = input('Укажите вес значения возраста партнера? (1-5): ')
    weight_client[3] = weight_interests = input('Укажите вес значения интересов партнера? (1-5): ')
    weight_client[4] = weight_relation = input('Укажите вес значения отношений партнера? (1-5): ')
    return weight_client


def main():
    original_client = who_is()
    # print("\nЭтап 1. Определили пользователя. Теперь определим его профиль. Press any key to continue:")
    # what_are_user_detail(original_client)
    print("\nЭтап N. Определим фото его профиля. Press any key to continue:")
    what_are_user_avatars(original_client)


if __name__ == '__main__':
    main()