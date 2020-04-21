import unittest
from unittest.mock import patch
import json
from BestTinderEver.main import *
from BestTinderEver.MongoWorker.dbwriter import *
from BestTinderEver.VKWorker.vkapp import *


class TestVK(unittest.TestCase):

    @patch('main.input', 5563153)
    def test_who_is(self):
        """
        Проверка на верного пользователя
        :return:
        """
        original_client = who_is()
        self.assertEqual(original_client, int())



if __name__ == '__main__':
    unittest.main()