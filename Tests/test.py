import json
import os
import unittest
import db
from Classes.item import Item
from Classes.user import User


class TestCases(unittest.TestCase):
    # Class-level variable to store the database object

    FAKE_USER_ID =  999999

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        json_path = os.path.join(current_dir, 'test.json')

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
        test_item_id = 300

        fake_item = Item(test_item_id)

        db.add_item_to_user(idUser=self.FAKE_USER_ID, item=fake_item)

        count = db.get_item_count_from_user(idUser=self.FAKE_USER_ID, idItem=fake_item.get_idItem())
        self.assertEqual(count, 1)

    def test_04_equip_item(self):
        test_item_id = 470

        fake_item = Item(test_item_id)

        idRel = db.add_item_to_user(idUser=self.FAKE_USER_ID, item=fake_item)
        fake_item.set_idRel(idRel)

        db.equip_item(idUser=self.FAKE_USER_ID, item=fake_item)
        res = db.has_equipped_item(idUser=self.FAKE_USER_ID, relId=idRel)
        self.assertTrue(res)

    def test_05_unequip_item(self):
        test_item_id = 400

        fake_item = Item(test_item_id)

        idRel = db.add_item_to_user(idUser=self.FAKE_USER_ID, item=fake_item)
        fake_item.set_idRel(idRel)

        db.equip_item(idUser=self.FAKE_USER_ID, item=fake_item)

        db.unequip(idUser=self.FAKE_USER_ID, item=fake_item)
        res = db.has_equipped_item(idUser=self.FAKE_USER_ID, relId=idRel)
        self.assertFalse(res)

    def test_06_give_souls(self):
        amount = 5000
        user = User(self.FAKE_USER_ID)
        old_rune_amount = user.get_runes()
        db.increase_runes_from_user_with_id(idUser=self.FAKE_USER_ID, amount=amount)
        user.update_user()
        new_rune_amount = user.get_runes()

        self.assertEqual(old_rune_amount + amount, new_rune_amount)

    def test_07_decrease_souls(self):
        amount = 5000
        user = User(self.FAKE_USER_ID)
        old_rune_amount = user.get_runes()
        db.decrease_runes_from_user_with_id(userId=self.FAKE_USER_ID, amount=amount)
        user.update_user()
        new_rune_amount = user.get_runes()

        self.assertEqual(old_rune_amount - amount, new_rune_amount)


if __name__ == '__main__':
    unittest.main()