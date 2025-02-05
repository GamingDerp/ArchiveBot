# If you're going to use the code in this file, rename it to "main.py", otherwise the bot won't work. -Derp

import os
import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from datetime import datetime, timedelta
import time

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True           
intents.messages = True         
intents.reactions = True

# Bot Intents & Defining Bot
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')    
bot.config = {
    "server_id": 840052141258309672,
}

# Loading Cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    await load()
    await bot.start("TOKEN")
    
# Startup Event
@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Connecting Stoneworks.."))
    await print(f"Logged in as {bot.user} \nID: {bot.user.id}")
    await bot.tree.sync()

asyncio.run(main())
