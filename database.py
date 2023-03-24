import discord
from discord.ext import commands
import json
import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1111',
    port='3306',
    database='tarnished'
)

cursor = mydb.cursor()

# Check if the connection is alive
if mydb.is_connected():
  print("Database connection successful")
else:
  print("Database connection failed")

# Define a function that accesses the cursor
def Get_Users():
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    return result