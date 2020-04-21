import unittest
from unittest.mock import patch
import json
from BestTinderEver.main import *
from BestTinderEver.MongoWorker.dbwriter import *
from BestTinderEver.VKWorker.vkapp import *


class TestVK(unittest.TestCase):

    def test_who_is_right(self):
        """
        Проверка функции
        :return:
        """
        with patch('builtins.input', return_value='171691064'):
            assert who_is() == 171691064


    def test_if_user_id_is_not_int(self):
        """
        Проверка функции
        :return:
        """
        with patch('builtins.input', return_value='eshmargunov'):
            assert who_is() == 171691064


if __name__ == '__main__':
    unittest.main()