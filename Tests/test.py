import json
import os
import unittest
import db
from Classes.item import Item


class TestCases(unittest.TestCase):
    # Class-level variable to store the database object

    FAKE_USER_ID =  999999

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        json_path = os.path.join(current_dir, 'unittestbot.json')

        with open(json_path) as file:
            botConfig = json.load(file)

        cls.db = db.init_database(botConfig)

    @classmethod
    def tearDownClass(self):
        db.reset_user(idUser=self.FAKE_USER_ID)

    def test_01_add_new_user(self):
        db.add_user(userId=self.FAKE_USER_ID, userName="UnitTest")

        self.assertIsNotNone(db.get_user_with_id(userId=self.FAKE_USER_ID))

    def test_02_does_user_exist(self):
        self.assertTrue(db.does_user_exist(self.FAKE_USER_ID))

    def test_03_add_item_to_user(self):
        test_item_id = 853

        fake_item = Item(test_item_id)

        db.add_item_to_user(idUser=self.FAKE_USER_ID, item=fake_item)

        count = db.get_item_count_from_user(idUser=self.FAKE_USER_ID, idItem=fake_item.get_idItem())
        self.assertEqual(count, 1)

    def test_04_equip_item(self):
        test_item_id = 853

        fake_item = Item(test_item_id)

        idRel = db.add_item_to_user(idUser=self.FAKE_USER_ID, item=fake_item)
        fake_item.set_idRel(idRel)

        result = db.equip_item(idUser=self.FAKE_USER_ID, item=fake_item)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()