import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import config
import json

cursor: MySQLCursor | CMySQLCursor = NotImplemented

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
    sql = "INSERT INTO user VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, null, null, null, null, null)"
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

        sql = f"INSERT INTO item VALUES (NULL,'{weapon_name}', {total_dmg}, {total_dmg * 6}, '{weapon['category']}', 'Weapon', {req_vigor}, {req_mind}, {req_endurance}, {req_strength}, {req_dexterity}, {req_intelligence}, {req_faith}, {req_arcane}, 1);"

        cursor.execute(sql)
        mydb.commit()

def get_json_req_attribute(weapon, attribute_name):
    try:
        req_value = next(attribute['amount'] for attribute in weapon['requiredAttributes'] if attribute['name'] == attribute_name)
    except StopIteration:
        req_value = 0
    return req_value