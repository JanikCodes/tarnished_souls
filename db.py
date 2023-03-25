import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
import config

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

def add_user(idUser, userName):
    sql = "INSERT INTO user VALUE(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, null, null, null, null, null)"
    val = (idUser, userName, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1)
    cursor.execute(sql, val)
    print("Added new user with userName" + userName)


def does_user_exist(idUser):
    print("INIT")
    sql = "SELECT * FROM user u WHERE u.idUser = %s"
    val = (idUser,)
    cursor.execute(sql, val)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False

def validate_user(idUser):
    print("Validate!")
