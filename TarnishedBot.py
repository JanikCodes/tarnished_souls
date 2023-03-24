import discord
import json

class TarnishedBot(discord.Client):
    async def on_ready(self):
        print("I'm logged in. Beep bop.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startwith("!stats"):
            completeText = message.content.split(" ")


#load bot token from json
with open('bot.json') as file:
    botConfig = json.load(file)


intents = discord.Intents.default()
bot = TarnishedBot(intents=intents)
bot.run(botConfig["token"])