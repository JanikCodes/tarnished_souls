import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1111',
    port='3386',
    database='tarnished'
)

mysql.connector.connect()