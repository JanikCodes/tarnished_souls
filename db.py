import random

import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import config
import json

from Classes.encounter import Encounter
from Classes.item import Item
async def init_database():
    global mydb
    # Connect to the database
    mydb = mysql.connector.connect(
        host=config.botConfig["host"],
        user=config.botConfig["user"],
        password=config.botConfig["password"],
        port=config.botConfig["port"],
        database=config.botConfig["database"],
    )

    global cursor
    cursor = mydb.cursor()

    # Check if the connection is alive
    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")


def add_user(userId, userName):
    sql = "INSERT INTO user VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, null, null, null, null, null)"
    val = (userId, userName, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1)
    cursor.execute(sql, val)
    mydb.commit()

    print("Added new user with userName: " + userName)


def get_user_with_id(userId):
    sql = "SELECT idUser, userName, level, xp, souls, vigor, mind, endurance, strength, dexterity, intelligence, " \
          "faith, arcane, last_explore, e_weapon, e_head, e_chest, e_legs FROM user u WHERE u.idUser = %s"
    val = (userId, )
    cursor.execute(sql, val)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None


def does_user_exist(idUser):
    sql = "SELECT * FROM user u WHERE u.idUser = %s"
    val = (idUser, )
    cursor.execute(sql, val)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def validate_user(userId, userName):
    if not does_user_exist(userId):
        add_user(userId, userName)


def get_stat_level_from_user_with_id(userId, value):
    sql = f"SELECT {value} FROM user u WHERE u.idUser = %s"
    val = (userId, )
    cursor.execute(sql, val)
    res = str(cursor.fetchone()).strip("(,)")
    if res:
        return res
    else:
        return 0

def increase_stat_from_user_with_id(userId, stat_name):
    sql = f"UPDATE user u SET {stat_name} = {stat_name} + 1 WHERE u.idUser = {userId};"
    cursor.execute(sql)
    mydb.commit()


def decrease_souls_from_user_with_id(userId, amount):
    sql = f"UPDATE user u SET souls = souls - {amount} WHERE u.idUser = {userId};"
    cursor.execute(sql)
    mydb.commit()


def fill_db_weapons():
    # read the JSON file
    with open('Data/weapons.json', 'r') as f:
        data = json.load(f)

    # iterate over the objects
    for weapon in data:
        weapon_name = weapon['name'].replace("'", "''")
        req_vigor = get_json_req_attribute(weapon, "Vig")
        req_mind = get_json_req_attribute(weapon, "Min")
        req_endurance = get_json_req_attribute(weapon, "End")
        req_strength = get_json_req_attribute(weapon, "Str")
        req_dexterity = get_json_req_attribute(weapon, "Dex")
        req_intelligence = get_json_req_attribute(weapon, "Int")
        req_faith = get_json_req_attribute(weapon, "Fai")
        req_arcane = get_json_req_attribute(weapon, "Arc")

        total_dmg = sum(attack['amount'] for attack in weapon['attack'])

        sql = f"INSERT INTO item VALUES (NULL,'{weapon_name}', {total_dmg}, {total_dmg * 6}, '{weapon['category']}', 'Weapon', {req_vigor}, {req_mind}, {req_endurance}, {req_strength}, {req_dexterity}, {req_intelligence}, {req_faith}, {req_arcane}, 1, {weapon['weight']});"

        cursor.execute(sql)
        mydb.commit()

def fill_db_armor():
    # read the JSON file
    with open('Data/armor.json', 'r') as f:
        data = json.load(f)

    # iterate over the objects
    for armor in data:
        armor_name = armor['name'].replace("'", "''")

        total_negation = sum(negation['amount'] for negation in armor['dmgNegation'])

        sql = f"INSERT INTO item VALUES (NULL,'{armor_name}', {total_negation}, {total_negation * 40}, '{armor['category']}', 'Armor', 0, 0, 0, 0, 0, 0, 0, 0, 1, {armor['weight']});"

        cursor.execute(sql)
        mydb.commit()

def get_json_req_attribute(weapon, attribute_name):
    try:
        req_value = next(attribute['amount'] for attribute in weapon['requiredAttributes'] if attribute['name'] == attribute_name)
    except StopIteration:
        req_value = 0
    return req_value


def get_encounters_from_user_with_id(idUser):
    encounters = []
    sql = f"SELECT e.idEncounter, e.description, e.dropRate FROM encounter e, user_encounter r WHERE r.idEncounter = e.idEncounter AND r.idUser = {idUser};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            encounters.append(Encounter(id=row[0], description=row[1], drop_rate=row[2]))

    return encounters


def get_item_from_user_encounter_with_enc_id(idUser, idEncounter):
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, r.extra, i.obtainable, i.weight FROM item i, user_encounter r WHERE r.idEncounter = {idEncounter} AND r.idUser = {idUser} AND r.idItem = i.idItem;"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5], reqEndurance=[6], reqStrength=res[7], reqDexterity=[8], reqIntelligence=res[9], reqFaith=res[10], reqArcane=res[11], value=res[12], price=res[13], obtainable=res[15], weight=res[16])
        item.set_extra_value(res[14])
        return item

def update_last_explore_timer_from_user_with_id(idUser, current_time):
    sql = f"UPDATE user u SET last_explore = {current_time} WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def get_all_unique_encounters_for_user(idUser):
    encounters = []
    sql = f"SELECT e.idEncounter, e.description, e.dropRate FROM encounter e WHERE e.idEncounter NOT IN (SELECT idEncounter FROM user_encounter r WHERE r.idUser = {idUser});"

    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            encounters.append(Encounter(id=row[0], description=row[1], drop_rate=row[2]))

    return encounters

def create_new_encounter(idUser):
    all_encounters = get_all_unique_encounters_for_user(idUser=idUser)

    selected_encounter = random.choice(all_encounters)

    sql = f"INSERT INTO user_encounter VALUE(NULL, {selected_encounter.get_id()}, {idUser}, NULL, 0);"
    cursor.execute(sql)
    mydb.commit()

    return selected_encounter


def remove_user_encounters(idUser):
    sql = f"DELETE FROM user_encounter r WHERE r.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

def get_all_item_ids():
    item_ids = []
    sql = f"SELECT i.idItem FROM item i;"

    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            item_ids.append(row[0])

    return item_ids

def add_item_to_user(idUser, item):
    sql = f"SELECT r.idRel FROM user_has_item r WHERE r.idUser = {idUser} AND r.idItem = {item.get_idItem()} AND r.level = {item.get_level()} AND r.value = {item.get_extra_value()};"
    cursor.execute(sql)

    res = cursor.fetchone()
    if res:
        # update count
        sql = f"UPDATE user_has_item r SET r.count = r.count + 1 WHERE r.idUser = {idUser} AND r.idItem = {item.get_idItem()} AND r.level = {item.get_level()} AND r.value = {item.get_extra_value()};"
        cursor.execute(sql)
        mydb.commit()
    else:
        # add new item to table
        sql = f"INSERT INTO user_has_item VALUE(NULL, {idUser}, {item.get_idItem()}, {item.get_level()}, 1, {item.get_extra_value()});"
        cursor.execute(sql)
        mydb.commit()

def get_item_from_item_id(idItem):
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight FROM item i WHERE i.idItem = {idItem}"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5], reqEndurance=res[6], reqStrength=res[7], reqDexterity=res[8], reqIntelligence=res[9], reqFaith=res[10], reqArcane=res[11], value=res[12], price=res[13], obtainable=res[14], weight=res[15])
        return item
    else:
        return None

def update_user_encounter_item(idEncounter, item, idUser):
    sql = f"SELECT r.idRel FROM user_encounter r WHERE r.idEncounter = {idEncounter} AND r.idUser = {idUser};"
    cursor.execute(sql)

    res = cursor.fetchone()
    if res:
        sql = f"UPDATE user_encounter r SET r.idItem = {item.get_idItem()}, r.extra = {item.get_extra_value()} WHERE r.idEncounter = {idEncounter} AND r.idUser = {idUser};"
        cursor.execute(sql)
        mydb.commit()

def get_items_from_user_id_with_type(idUser, type):
    items = []
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight, r.level, r.count, r.value FROM item i, user_has_item r WHERE i.idItem = r.idItem AND r.idUser = {idUser} AND i.type = '{type}';"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            item = Item(idItem=row[0], name=row[1], iconCategory=row[2], item_type=row[3], reqVigor=row[4], reqMind=row[5], reqEndurance=row[6], reqStrength=row[7], reqDexterity=row[8], reqIntelligence=row[9], reqFaith=row[10], reqArcane=row[11], value=row[12], price=row[13], obtainable=row[14], weight=row[15])
            item.set_level(row[16])
            item.set_count(row[17])
            item.set_extra_value(row[18])
            items.append(item)
        return items
    else:
        return None