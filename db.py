import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import config
from Classes.user import User

cursor: MySQLCursor | CMySQLCursor = NotImplemented
mydb = None

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
    print("Added new user with userName: " + userName)

def get_user_with_id(userId):
    sql = "SELECT idUser, userName, level, xp, souls, vigor, mind, endurance, strength, dexterity, intelligence, faith, arcane, last_explore, e_weapon, e_head, e_chest, e_legs FROM user u WHERE u.idUser = %s"
    val = (userId)
    cursor.execute(sql, val)
    res = cursor.fetchone()
    if res:
        user = User()
        user.set_userId(res[0])
        user.set_userName(res[1])
        user.set_level(res[2])
        user.set_xp(res[3])
        user.set_souls(res[4])
        user.set_vigor(res[5])
        user.set_mind(res[6])
        user.set_endurance(res[7])
        user.set_strength(res[8])
        user.set_dexterity(res[9])
        user.set_intelligence(res[10])
        user.set_faith(res[11])
        user.set_arcane(res[12])
        user.set_last_explore(res[13])
        user.set_e_weapon(res[14])
        user.set_e_head(res[15])
        user.set_e_chest(res[16])
        user.set_e_legs(res[17])
        print(user)
        return user
    else:
        return None

def does_user_exist(idUser):
    sql = "SELECT * FROM user u WHERE u.idUser = %s"
    val = (idUser,)
    cursor.execute(sql, val)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False

def validate_user(userId, userName):
    if not does_user_exist(userId):
        add_user(userId, userName)
    else:
        print("It exists")