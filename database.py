import discord
from discord.ext import commands
import json
import mysql.connector
import TarnishedBot

# Connect to the database
mydb = mysql.connector.connect(
    host= TarnishedBot.botConfig["host"],
    user= TarnishedBot.botConfig["user"],
    password= TarnishedBot.botConfig["password"],
    port= TarnishedBot.botConfig["port"],
    database= TarnishedBot.botConfig["database"],
)

cursor = mydb.cursor()

# Check if the connection is alive
if mydb.is_connected():
  print("Database connection successful")
else:
  print("Database connection failed")

def add_user():
    cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    return result