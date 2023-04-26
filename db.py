import json
import random

import mysql.connector

import config
from Classes.encounter import Encounter
from Classes.enemy import Enemy
from Classes.enemy_move import EnemyMove
from Classes.item import Item
from Classes.location import Location
from Classes.quest import Quest
from Classes.quest_progress import QuestProgress


async def init_database():
    global mydb
    # Connect to the database
    mydb = mysql.connector.connect(
        host=config.botConfig["host"],
        user=config.botConfig["user"],
        password=config.botConfig["password"],
        port=config.botConfig["port"],
        database=config.botConfig["database"],
        charset='utf8mb4'
    )

    global cursor
    cursor = mydb.cursor()

    # Check if the connection is alive
    if mydb.is_connected():
        print("Database connection successful")
    else:
        print("Database connection failed")


def add_user(userId, userName):
    sql = f"INSERT INTO user VALUE({userId}, '{userName}', 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, null, null, null, null, null, 1, 1, 0, 0)"
    cursor.execute(sql)
    mydb.commit()

    print("Added new user with userName: " + userName)


def get_item_name_from_id(item_id):
    if item_id != "":
        sql = f"SELECT name FROM item WHERE iditem = {item_id};"
        cursor.execute(sql)
        return cursor.fetchone()
    else:
        return None

# data insertion
def add_enemy(enemy_id, logic_id, name, description, health, runes, location_id):
    loc_id = str(location_id).strip("'(,)'")
    log_id = str(logic_id).strip("'(,)'")
    sql = f"INSERT INTO enemy VALUES({int(enemy_id)}, {int(log_id)}, '{name}', '{description}', {int(health)}, {int(runes)}, {int(loc_id)});"
    cursor.execute(sql)
    mydb.commit()
    return sql


def add_enemy_move(description, phase, type_id, enemy_id, damage, healing, duration, max_targets):
    sql = f"INSERT INTO enemy_moves VALUES(null, '{description}', {int(phase)}, {int(type_id)}, {int(enemy_id)}, {damage}, {healing}, {duration}, {int(max_targets)})"
    cursor.execute(sql)
    mydb.commit()
    return sql


def add_encounter(description, dropRate, location_id):
    sql = f"INSERT INTO encounter VALUES(null, '{description}', {int(dropRate)}, {int(location_id)})"
    cursor.execute(sql)
    mydb.commit()
    return sql


def add_quest(quest: Quest()):
    Enemy = quest.get_enemy()
    enemy_id = None
    if Enemy is not None:
        enemy_id = Enemy.get_id()
    else:
        enemy_id = "null"

    exploration_location = quest.get_explore_location()
    exploration_location_id = int(str(exploration_location.get_id())) if exploration_location != 0 else "null"

    location_reward = quest.get_location_reward()
    location_reward_id = int(str(location_reward.get_id())) if location_reward != 0 else "null"
    sql = f"INSERT INTO quest VALUES(null, '{quest.get_title()}', '{quest.get_description()}', {quest.get_req_kills()}, {quest.get_req_item_count()}, {quest.get_req_runes()}, {quest.get_item()}, {enemy_id}, {quest.get_rune_reward()}, {location_reward_id}, {quest.get_req_explore_count()}, {exploration_location_id}, {quest.get_cooldown()});"
    cursor.execute(sql)
    mydb.commit()
    return sql


def add_quest_has_item(quest_id, item_reward_id, count):
    sql = f"INSERT INTO quest_has_item VALUES(null, {quest_id}, {item_reward_id}, {count})"
    cursor.execute(sql)
    mydb.commit()
    return sql

def get_quest_id_from_title_and_desc(title, desc):
    sql = f"SELECT idquest FROM quest WHERE title='{title}' AND description='{desc}'"
    cursor.execute(sql)
    return cursor.fetchone()

def get_enemy_and_desc():
    sql = "SELECT name, description FROM enemy;"
    cursor.execute(sql)
    return cursor.fetchall()


def get_enemy_id_from_name(name):
    sql = f"SELECT idenemy FROM enemy WHERE name='{name}'"
    cursor.execute(sql)
    return cursor.fetchone()


# data insertion
def get_enemy_count():
    sql = "SELECT COUNT(*) FROM enemy"
    cursor.execute(sql)
    return cursor.fetchone()


# data insertion
def get_all_enemy_logic():
    sql = "SELECT name FROM enemy_logic"
    cursor.execute(sql)
    return cursor.fetchall()


def get_enemy_logic_id_from_name(name):
    sql = "SELECT idLogic FROM enemy_logic WHERE name=%s"
    val = name
    cursor.execute(sql, (val,))
    return cursor.fetchone()


def get_all_move_types():
    sql = "SELECT name FROM move_type"
    cursor.execute(sql)
    return cursor.fetchall()


def get_move_type_id_from_name(name):
    sql = f"SELECT idType FROM move_type WHERE name='{name}'"
    cursor.execute(sql)
    return cursor.fetchone()


def get_encounter_id_from_description(description):
    sql = f"SELECT idencounter FROM encounter WHERE description='{description}'"
    cursor.execute(sql)
    return cursor.fetchone()


# data insertion
def get_all_locations():
    sql = "SELECT name, description FROM location"
    cursor.execute(sql)
    return cursor.fetchall()


def get_location_id_from_name(name):
    sql = "SELECT idLocation FROM location WHERE name=%s"
    val = name
    cursor.execute(sql, (val,))
    return cursor.fetchone()


def get_user_with_id(userId):
    sql = f"SELECT idUser, userName, level, xp, souls, vigor, mind, endurance, strength, dexterity, intelligence, " \
          f"faith, arcane, last_explore, e_weapon, e_head, e_chest, e_legs, e_gauntlet, currentLocation, maxLocation, NG, last_quest FROM user u WHERE u.idUser = {userId};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None


def does_user_exist(idUser):
    sql = f"SELECT * FROM user u WHERE u.idUser = {idUser}"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def validate_user(userId):
    if not does_user_exist(userId):
        return False

    return True


def get_stat_level_from_user_with_id(userId, value):
    sql = f"SELECT {value} FROM user u WHERE u.idUser = {userId};"
    cursor.execute(sql)
    res = str(cursor.fetchone()).strip("(,)")
    if res:
        return res
    else:
        return 0


def increase_stat_from_user_with_id(userId, stat_name):
    sql = f"UPDATE user u SET {stat_name} = {stat_name} + 1 WHERE u.idUser = {userId};"
    cursor.execute(sql)
    mydb.commit()


def set_stat_from_user_with_id(userId, stat_name, value):
    sql = f"UPDATE user u SET {stat_name} = {value} WHERE u.idUser = {userId};"
    cursor.execute(sql)
    mydb.commit()


def decrease_runes_from_user_with_id(userId, amount):
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

        scl_vigor = get_json_scale_attribute(weapon, "Vig")
        scl_mind = get_json_scale_attribute(weapon, "Min")
        scl_endurance = get_json_scale_attribute(weapon, "End")
        scl_strength = get_json_scale_attribute(weapon, "Str")
        scl_dexterity = get_json_scale_attribute(weapon, "Dex")
        scl_intelligence = get_json_scale_attribute(weapon, "Int")
        scl_faith = get_json_scale_attribute(weapon, "Fai")
        scl_arcane = get_json_scale_attribute(weapon, "Arc")

        total_dmg = sum(attack['amount'] for attack in weapon['attack'])

        sql = f"INSERT INTO item VALUES (NULL,'{weapon_name}', {total_dmg}, {total_dmg * 6}, '{weapon['category']}', 'Weapon', {req_vigor}, {req_mind}, {req_endurance}, {req_strength}, {req_dexterity}, {req_intelligence}, {req_faith}, {req_arcane}, 1, {weapon['weight']}, '{weapon['image']}', '{scl_vigor}', '{scl_mind}', '{scl_endurance}', '{scl_strength}', '{scl_dexterity}', '{scl_intelligence}', '{scl_faith}', '{scl_arcane}' );"

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

        sql = f"INSERT INTO item VALUES (NULL,'{armor_name}', {total_negation}, {total_negation * 40}, '{armor['category']}', 'Armor', 0, 0, 0, 0, 0, 0, 0, 0, 1, {armor['weight']}, '{armor['image']}', '-', '-', '-', '-', '-', '-', '-', '-');"

        cursor.execute(sql)
        mydb.commit()


def get_json_req_attribute(item, attribute_name):
    try:
        req_value = next(attribute['amount'] for attribute in item['requiredAttributes'] if attribute['name'] == attribute_name)
    except StopIteration:
        req_value = 0
    return req_value


def get_json_scale_attribute(item, attribute_name):
    req_value = "-"
    for attribute in item['scalesWith']:
        if attribute['name'] == attribute_name and 'scaling' in attribute:
            req_value = attribute['scaling']
            break
    return req_value


def get_encounters_from_user(user):
    encounters = []
    sql = f"SELECT e.idEncounter, e.description, e.dropRate, e.idLocation FROM encounter e, user_encounter r WHERE r.idEncounter = e.idEncounter AND r.idUser = {user.get_userId()} AND e.idLocation = {user.get_current_location().get_id()};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            encounters.append(Encounter(id=row[0], description=row[1], drop_rate=row[2], idLocation=row[3]))

    return encounters


def get_item_from_user_encounter_with_enc_id(idUser, idEncounter):
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, r.extra, i.obtainable, i.weight, i.iconUrl, i.sclVigor, i.sclMind, i.sclEndurance, i.sclStrength, i.sclDexterity, i.sclIntelligence, i.sclFaith, i.sclArcane FROM item i, user_encounter r WHERE r.idEncounter = {idEncounter} AND r.idUser = {idUser} AND r.idItem = i.idItem;"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5],
                    reqEndurance=[6], reqStrength=res[7], reqDexterity=[8], reqIntelligence=res[9], reqFaith=res[10],
                    reqArcane=res[11], value=res[12], price=res[13], obtainable=res[15], weight=res[16],
                    iconUrl=res[17], sclVigor=res[18], sclMind=res[19], sclEndurance=res[20], sclStrength=res[21], sclDexterity=res[22], sclIntelligence=res[23], sclFaith=res[24], sclArcane=res[25])
        item.set_extra_value(res[14])
        return item


def update_last_explore_timer_from_user_with_id(idUser, current_time):
    sql = f"UPDATE user u SET last_explore = {current_time} WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def get_all_unique_encounters_for_user_from_location(idUser, idLocation):
    encounters = []
    sql = f"SELECT e.idEncounter, e.description, e.dropRate, e.idLocation FROM encounter e WHERE e.idEncounter NOT IN (SELECT idEncounter FROM user_encounter r WHERE r.idUser = {idUser}) AND e.idLocation = {idLocation};"

    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            encounters.append(Encounter(id=row[0], description=row[1], drop_rate=row[2], idLocation=row[3]))

    return encounters


def create_new_encounter_from_location(idUser, idLocation):
    all_encounters = get_all_unique_encounters_for_user_from_location(idUser=idUser, idLocation=idLocation)

    if len(all_encounters) > 0:
        selected_encounter = random.choice(all_encounters)

        sql = f"INSERT INTO user_encounter VALUE(NULL, {selected_encounter.get_id()}, {idUser}, NULL, 0);"
        cursor.execute(sql)
        mydb.commit()

        return selected_encounter
    return None


def remove_user_encounters(idUser):
    sql = f"DELETE FROM user_encounter WHERE idUser = {idUser};"
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
        sql = f"UPDATE user_has_item r SET r.count = r.count + {item.get_count()} WHERE r.idUser = {idUser} AND r.idItem = {item.get_idItem()} AND r.level = {item.get_level()} AND r.value = {item.get_extra_value()};"
        cursor.execute(sql)
        mydb.commit()
    else:
        # add new item to table
        sql = f"INSERT INTO user_has_item VALUE(NULL, {idUser}, {item.get_idItem()}, {item.get_level()}, {item.get_count()}, {item.get_extra_value()});"
        cursor.execute(sql)
        mydb.commit()


def add_item_to_user_with_item_name(idUser, item_name):
    item = get_item_from_item_name(item_name=item_name)

    # add new item to table
    sql = f"INSERT INTO user_has_item VALUE(NULL, {idUser}, {item.get_idItem()}, {item.get_level()}, 1, {item.get_extra_value()});"
    cursor.execute(sql)
    mydb.commit()

    sql = f"SELECT r.idRel FROM user_has_item r WHERE r.idUser = {idUser} AND r.idItem = {item.get_idItem()} AND r.level = {item.get_level()} AND r.count = 1 and r.value = {item.get_extra_value()};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item.set_idRel(res[0])
        return item

    return None


def get_item_from_item_id(idItem):
    if idItem is None:
        return None

    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight, i.iconUrl, i.sclVigor, i.sclMind, i.sclEndurance, i.sclStrength, i.sclDexterity, i.sclIntelligence, i.sclFaith, i.sclArcane FROM item i WHERE i.idItem = {idItem}"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5],
                    reqEndurance=res[6], reqStrength=res[7], reqDexterity=res[8], reqIntelligence=res[9],
                    reqFaith=res[10], reqArcane=res[11], value=res[12], price=res[13], obtainable=res[14],
                    weight=res[15], iconUrl=res[16], sclVigor=res[17], sclMind=res[18], sclEndurance=res[19], sclStrength=res[20], sclDexterity=res[21], sclIntelligence=res[22], sclFaith=res[23], sclArcane=res[24])
        return item
    else:
        return None


def get_item_from_item_name(item_name):
    sql = f'SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight, i.iconUrl, i.sclVigor, i.sclMind, i.sclEndurance, i.sclStrength, i.sclDexterity, i.sclIntelligence, i.sclFaith, i.sclArcane FROM item i WHERE i.name = "{item_name}"'
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5],
                    reqEndurance=res[6], reqStrength=res[7], reqDexterity=res[8], reqIntelligence=res[9],
                    reqFaith=res[10], reqArcane=res[11], value=res[12], price=res[13], obtainable=res[14],
                    weight=res[15], iconUrl=res[16], sclVigor=res[17], sclMind=res[18], sclEndurance=res[19], sclStrength=res[20], sclDexterity=res[21], sclIntelligence=res[22], sclFaith=res[23], sclArcane=res[24])
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


def get_items_from_user_id_with_type_at_page(idUser, type, page, max_page):
    items = []
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight, r.level, r.count, r.value, r.idRel, i.iconUrl, i.sclVigor, i.sclMind, i.sclEndurance, i.sclStrength, i.sclDexterity, i.sclIntelligence, i.sclFaith, i.sclArcane FROM item i, user_has_item r WHERE i.idItem = r.idItem AND r.idUser = {idUser} AND i.type = '{type}' ORDER BY i.value + r.value DESC LIMIT {max_page} OFFSET {(page - 1) * max_page};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            item = Item(idItem=row[0], name=row[1], iconCategory=row[2], item_type=row[3], reqVigor=row[4],
                        reqMind=row[5], reqEndurance=row[6], reqStrength=row[7], reqDexterity=row[8],
                        reqIntelligence=row[9], reqFaith=row[10], reqArcane=row[11], value=row[12], price=row[13],
                        obtainable=row[14], weight=row[15], iconUrl=row[20], sclVigor=row[21], sclMind=row[22], sclEndurance=row[23], sclStrength=row[24], sclDexterity=row[25], sclIntelligence=row[26], sclFaith=row[27], sclArcane=row[28])
            item.set_level(row[16])
            item.set_count(row[17])
            item.set_extra_value(row[18])
            item.set_idRel(row[19])
            items.append(item)
        return items
    else:
        return None


def get_item_from_user_with_id_rel(idUser, idRel):
    sql = f"SELECT i.idItem, i.name, i.iconCategory, i.type, i.reqVigor, i.reqMind, i.reqEndurance, i.reqStrength, i.reqDexterity, i.reqIntelligence, i.reqFaith, i.reqArcane, i.value, i.price, i.obtainable, i.weight, r.level, r.count, r.value, r.idRel, i.iconUrl, i.sclVigor, i.sclMind, i.sclEndurance, i.sclStrength, i.sclDexterity, i.sclIntelligence, i.sclFaith, i.sclArcane FROM item i, user_has_item r WHERE i.idItem = r.idItem AND r.idUser = {idUser} AND r.idRel = '{idRel}';"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        item = Item(idItem=res[0], name=res[1], iconCategory=res[2], item_type=res[3], reqVigor=res[4], reqMind=res[5],
                    reqEndurance=res[6], reqStrength=res[7], reqDexterity=res[8], reqIntelligence=res[9],
                    reqFaith=res[10], reqArcane=res[11], value=res[12], price=res[13], obtainable=res[14],
                    weight=res[15], iconUrl=res[20], sclVigor=res[21], sclMind=res[22], sclEndurance=res[23], sclStrength=res[24], sclDexterity=res[25], sclIntelligence=res[26], sclFaith=res[27], sclArcane=res[28])
        item.set_level(res[16])
        item.set_count(res[17])
        item.set_extra_value(res[18])
        item.set_idRel(res[19])
        return item
    else:
        return None


def equip_item(idUser, item):
    equip_slot_name = str()

    match item.get_iconCategory():
        case 'leg_armor':
            equip_slot_name = 'e_legs'
        case 'chest_armor':
            equip_slot_name = 'e_chest'
        case 'helm':
            equip_slot_name = 'e_head'
        case 'gauntlets':
            equip_slot_name = 'e_gauntlet'
        case _:
            equip_slot_name = 'e_weapon'

    sql = f"SELECT r.idRel FROM user_has_item r WHERE r.idRel = {item.get_idRel()} AND r.idUser = {idUser};"
    cursor.execute(sql)

    res = cursor.fetchone()
    if res:
        sql = f"UPDATE user u SET u.{equip_slot_name} = {item.get_idRel()} WHERE u.idUser = {idUser};"
        cursor.execute(sql)
        mydb.commit()

        return True

    return False


def get_item_count_from_user(idUser, type):
    sql = f"SELECT count(*) FROM user_has_item r, item i WHERE i.idItem = r.idItem AND r.idUser = {idUser} AND i.type = '{type}';"
    cursor.execute(sql)
    res = str(cursor.fetchone()).strip("(,)")
    if res:
        return res
    else:
        return 0


def get_enemy_with_id(idEnemy):
    sql = f"SELECT name, idLogic, description, health, runes, idLocation FROM enemy WHERE idEnemy = {idEnemy};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None


def get_enemy_logic_with_id(idLogic):
    sql = f"SELECT idLogic, name FROM enemy_logic WHERE idLogic = {idLogic};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None


def get_enemy_moves_with_enemy_id(idEnemy):
    enemy_moves = []
    sql = f"select m.idMove, m.description, m.phase, m.idType, m.damage, m.healing, m.duration, m.maxTargets FROM enemy_moves m WHERE m.idEnemy = {idEnemy};"

    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            enemy_moves.append(EnemyMove(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return enemy_moves


def increase_runes_from_user_with_id(idUser, amount):
    sql = f"UPDATE user u SET souls = souls + {amount} WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def reset_user(idUser):
    sql = f"DELETE FROM user_has_quest r WHERE r.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"DELETE FROM user_encounter e WHERE e.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"DELETE FROM user_has_item r WHERE r.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"DELETE FROM user u WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def unequip(idUser, item):
    match item.get_iconCategory():
        case 'leg_armor':
            equip_slot_name = 'e_legs'
        case 'chest_armor':
            equip_slot_name = 'e_chest'
        case 'helm':
            equip_slot_name = 'e_head'
        case 'gauntlets':
            equip_slot_name = 'e_gauntlet'
        case _:
            equip_slot_name = 'e_weapon'

    sql = f"UPDATE user u SET u.{equip_slot_name} = NULL WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

def check_if_add_all_items():
    sql = f"SELECT count(*) from item;"
    cursor.execute(sql)
    res = str(cursor.fetchone()).strip("(,)")
    if res:
        return res
    else:
        return None


def get_location_from_id(idLocation):
    if idLocation:
        try:
            sql = f"SELECT idLocation, name, description FROM location WHERE idLocation = {idLocation};"
            cursor.execute(sql)
            res = cursor.fetchone()
            if res:
                location = Location(res[0], res[1], res[2])
                return location
            else:
                return None
        except mysql.connector.Error as err:
            # used for quest insertion when None
            return 0
    return None


def get_user_quest_with_user_id(idUser):
    sql = f"SELECT idRel, idQuest, idUser, remaining_kills, remaining_items, remaining_runes, remaining_explores FROM user_has_quest WHERE idUser = {idUser};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        quest_progress = QuestProgress(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
        return quest_progress
    else:
        return None


def get_quest_with_id(idQuest):
    sql = f"SELECT idQuest, title, description, reqKills, reqItemCount, reqRunes, idItem, idEnemy, runeReward, locationIdReward, reqExploreCount, locationId, cooldown FROM quest WHERE idQuest = {idQuest};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        quest = Quest(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11], res[12])
        return quest
    else:
        return None


def add_init_quest_to_user(idUser):
    first_quest = get_quest_with_id(1)
    sql = convert_python_none_to_null(f"INSERT INTO user_has_quest VALUE(NULL, {first_quest.get_id()}, {idUser}, {first_quest.get_req_kills()}, {first_quest.get_req_item_count()}, {first_quest.get_req_runes()}, {first_quest.get_req_explore_count()});")
    cursor.execute(sql)
    mydb.commit()

    return get_user_quest_with_user_id(idUser=idUser)


def remove_quest_from_user_with_quest_id(idUser, idQuest):
    sql = f"DELETE FROM user_has_quest WHERE idUser = {idUser} AND idQuest = {idQuest};"
    cursor.execute(sql)
    mydb.commit()

def add_quest_to_user(idUser, idQuest):
    quest = get_quest_with_id(idQuest)
    sql = convert_python_none_to_null(f"INSERT INTO user_has_quest VALUE(NULL, {quest.get_id()}, {idUser}, {quest.get_req_kills()}, {quest.get_req_item_count()}, {quest.get_req_runes()}, {quest.get_req_explore_count()});")
    cursor.execute(sql)
    mydb.commit()

def check_for_quest_update(idUser, idItem = 0, runes = 0, idEnemy = 0, explore_location_id = None):
    print("Checking for quest update..")
    sql = f"select q.idQuest, remaining_kills, remaining_items, remaining_runes, remaining_explores FROM quest q JOIN user_has_quest r ON q.idQuest = r.idQuest AND r.idUser = {idUser};"
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        quest = get_quest_with_id(res[0])

        if quest.get_item():
            if quest.get_item().get_idItem() == int(idItem):
                print("Quest: Updated item count")
                sql = f"UPDATE user_has_quest r SET r.remaining_items = GREATEST(remaining_items - 1, 0) WHERE r.idUser = {idUser};"
                cursor.execute(sql)
                mydb.commit()

        if quest.get_enemy():
            if quest.get_enemy().get_id() == int(idEnemy):
                print("Quest: Updated enemy count")
                sql = f"UPDATE user_has_quest r SET r.remaining_kills = GREATEST(remaining_kills - 1, 0) WHERE r.idUser = {idUser};"
                cursor.execute(sql)
                mydb.commit()

        if runes > 0:
            print("Quest: Updated runes count")
            sql = f"UPDATE user_has_quest r SET r.remaining_runes = GREATEST(remaining_runes - {runes}, 0) WHERE r.idUser = {idUser};"
            cursor.execute(sql)
            mydb.commit()

        if explore_location_id:
            if quest.get_explore_location():
                if quest.get_explore_location().get_id() == int(explore_location_id):
                    print("Quest: Updated explore count")
                    sql = f"UPDATE user_has_quest r SET r.remaining_explores = GREATEST(remaining_explores - 1, 0) WHERE r.idUser = {idUser};"
                    cursor.execute(sql)
                    mydb.commit()


def get_all_locations_from_user(user):
    locations = []

    sql = f"SELECT idLocation, name, description FROM location WHERE idLocation <= {user.get_max_location().get_id()} ORDER BY idLocation;"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            locations.append(Location(row[0], row[1], row[2]))

    return locations


def update_location_from_user(idUser, idLocation):
    sql = f"UPDATE user Set currentLocation = {idLocation} WHERE idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def update_max_location_from_user(idUser, idLocation):
    sql = f"UPDATE user Set maxLocation = {idLocation} WHERE idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()


def get_all_enemies_from_location(idLocation):
    enemies = []

    sql = f"SELECT idEnemy FROM enemy WHERE idLocation = {idLocation};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            enemies.append(Enemy(row[0]))

    return enemies


def get_quest_item_reward(idQuest):
    items = []

    sql = f"SELECT idItem, count FROM quest_has_item WHERE idQuest = {idQuest};"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for row in res:
            new_item = get_item_from_item_id(row[0])
            if new_item:
                new_item.set_count(row[1])
                items.append(new_item)

    return items


def update_last_quest_timer_from_user_with_id(idUser, current_time):
    sql = f"UPDATE user u SET last_quest = {current_time} WHERE u.idUser = {idUser};"
    cursor.execute(sql)
    mydb.commit()

def convert_python_none_to_null(sql):
    return sql.replace("None", "Null")

def complete_quest(user):
    sql = f"UPDATE user_has_quest u SET remaining_kills = 0 WHERE u.idUser = {user.get_userId()};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"UPDATE user_has_quest u SET remaining_items = 0 WHERE u.idUser = {user.get_userId()};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"UPDATE user_has_quest u SET remaining_runes = 0 WHERE u.idUser = {user.get_userId()};"
    cursor.execute(sql)
    mydb.commit()

    sql = f"UPDATE user_has_quest u SET remaining_explores = 0 WHERE u.idUser = {user.get_userId()};"
    cursor.execute(sql)
    mydb.commit()