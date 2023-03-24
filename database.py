import mysql.connector
import TarnishedBot

# Connect to the database
mydb = mysql.connector.connect(
    host=TarnishedBot.botConfig["host"],
    user=TarnishedBot.botConfig["user"],
    password=TarnishedBot.botConfig["password"],
    port=TarnishedBot.botConfig["port"],
    database=TarnishedBot.botConfig["database"],
)

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
