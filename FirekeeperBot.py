import discord
import json

class MyFirekeeperBot(discord.Client):
    async def on_ready(self):
        print("I'm logged in. Beep bop.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startwith("!stats"):
            completeText = message.content.split(" ")

intents = discord.Intents.all()

with open('bot.json') as file:
    botConfig = json.load(file)

bot = MyFirekeeperBot(intents=intents)
bot.run(botConfig["token"])