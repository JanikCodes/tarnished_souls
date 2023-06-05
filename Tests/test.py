import json
import os
import unittest

import db
from Classes.enemy import Enemy
from Classes.item import Item
from Classes.user import User


class TestCases(unittest.TestCase):
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

    def test_08_quest_explored_wrong_location(self):
        # explore 3 times the wrong quest
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=6)
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=6)
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=6)

        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        self.assertFalse(current_quest.is_finished())

    def test_09_quest_explored_right_location_but_didnt_complete_quest(self):
        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        old_count = current_quest.get_remaining_explore_count()

        # do it 2 times to nearly complete the quest
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=current_quest.quest.get_explore_location().get_id())
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=current_quest.quest.get_explore_location().get_id())

        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        new_count = current_quest.get_remaining_explore_count()

        self.assertEqual(old_count - 2, new_count)

    def test_10_quest_explored_right_location_and_complete_quest(self):
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, explore_location_id=1)
        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        self.assertTrue(current_quest.is_finished())

    def test_11_quest_remove_completed_quest(self):
        old_current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        db.remove_quest_from_user_with_quest_id(idUser=self.FAKE_USER_ID, idQuest=old_current_quest.quest.get_id())

        db.add_quest_to_user(idUser=self.FAKE_USER_ID, idQuest=old_current_quest.get_quest().get_id() + 1)

        new_current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        self.assertNotEqual(old_current_quest.quest.get_id(), new_current_quest.quest.get_id())

    def test_12_quest_kill_wrong_enemy(self):
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, idEnemy=20)
        db.check_for_quest_update(idUser=self.FAKE_USER_ID, idEnemy=20)

        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        self.assertEqual(current_quest.get_remaining_kills(), current_quest.quest.get_req_kills())

    def test_13_quest_kill_right_enemy(self):
        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        for index in range(0, current_quest.quest.get_req_kills()):
            db.check_for_quest_update(idUser=self.FAKE_USER_ID, idEnemy=current_quest.quest.get_enemy().get_id())

        current_quest = db.get_current_user_quest(idUser=self.FAKE_USER_ID)

        self.assertEqual(current_quest.get_remaining_kills(), 0)

    def test_14_search_inventory_item(self):
        fake_item = Item(idItem=1)
        db.add_item_to_user(self.FAKE_USER_ID, fake_item)

        searches = db.search_with_name(idUser=self.FAKE_USER_ID, name=fake_item.get_name(), filter="inventory", page=1, max_page=1)
        self.assertIsNotNone(searches)

    def test_15_search_item(self):
        fake_item = Item(idItem=1)

        searches = db.search_with_name(idUser=self.FAKE_USER_ID, name=fake_item.get_name(), filter="inventory", page=1,
                                       max_page=1)
        self.assertIsNotNone(searches)

    def test_16_search_enemy(self):
        fake_enemy = Enemy(idEnemy=1)

        searches = db.search_with_name(idUser=self.FAKE_USER_ID, name=fake_enemy.get_name().replace("'", ""), filter="enemy", page=1, max_page=1)

        self.assertIsNotNone(searches)