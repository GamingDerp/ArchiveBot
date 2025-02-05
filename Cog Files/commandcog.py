import os
import re
import time
import asyncio
import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True           
intents.messages = True         
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.launch_time = datetime.utcnow()
bot_id = 1143360299534143640
sda_logo = "https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg"
sda_color = 0x0E0E0E

# Server Commands Embed
se = discord.Embed(color=sda_color)
se.set_author(name="Bot Commands", icon_url=sda_logo)
se.set_thumbnail(url=sda_logo)
se.add_field(
    name="🔍 __Server Commands__",
    value=f"> `Search`, `Random`",
)

# General Commands Embed
ge = discord.Embed(color=sda_color)
ge.set_author(name="Bot Commands", icon_url=sda_logo)
ge.set_thumbnail(url=sda_logo)
ge.add_field(
    name="📌 __General Commands__",
    value=f"> `Help`, `Info`, `Test`",
)

# Help Menu Dropdown
class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Server Commands", description="Search, Random", emoji="🔍"),
            discord.SelectOption(label="General Commands",description="Help, Info, Test", emoji="📌"),
        ]
        super().__init__(min_values=1, max_values=1, options=options)

    async def callback(self, interaction:discord.Interaction):
        if self.values[0] == "Server Commands":
            await interaction.response.edit_message(embed=se)
        if self.values[0] == "General Commands":
            await interaction.response.edit_message(embed=ge)
    
# DropdownView Class
class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())      
        
# Commands Class
class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(bot_id) in message.content:
            await message.channel.send("I've been summoned! If you need me do `/help` <:CatWave2:1180121318658682971>")
    
    # Test command
    @bot.tree.command(description="Sends a message if the bot is online")
    async def test(self, interaction: discord.Interaction):
            await interaction.response.send_message("I'm up and indexing! <a:DerpPet:1146087107606098022>", ephemeral=True)
    
    # Help Command
    @bot.tree.command(description="Sends ArchiveBot's help menu")
    async def help(self, interaction: discord.Interaction):
        e = discord.Embed(color=sda_color)
        e.set_author(name="Bot Commands", icon_url=sda_logo)
        e.set_thumbnail(url=sda_logo)
        e.add_field(
            name="✧ __Command Menus__",
            value=f"> 🔍 Server"
                  f"\n> 📌 General"
        )
        view = DropdownView()
        await interaction.response.send_message(embed=e, view=view, ephemeral=True)
    
    # Info Command
    @bot.tree.command(description="Sends information about ArchiveBot")
    async def info(self, interaction: discord.Interaction):
        try:
            index_cog = self.bot.get_cog('IndexCog')
            if index_cog:
                index_server_count = sum(sum(len(links) for links in section.values()) for section in index_cog.index.values())
            else:
                index_server_count = 0
            total_lines = 30
            cog_directory = "./cogs"
            for filename in os.listdir(cog_directory):
                if filename.endswith(".py"):
                    with open(os.path.join(cog_directory, filename), "r") as file:
                        lines = file.readlines()
                        non_empty_lines = [line.strip() for line in lines if line.strip()]
                        total_lines += len(non_empty_lines)
            delta_uptime = datetime.utcnow() - bot.launch_time
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            e = discord.Embed(color=sda_color)
            e.set_author(name="Bot Information", icon_url=sda_logo)
            e.set_thumbnail(url=sda_logo)
            e.add_field(
                name="✧ __Index__",
                value=f"> **Servers:** {index_server_count}",
                inline=False
            )
            e.add_field(
                name="✧ __Statistics__",
                value=f"> **Commands:** [5]"
	              f"\n> **Code:** {total_lines} Lines"
                      f"\n> **Ping:** {round(self.bot.latency * 1000)}ms"
                      f"\n> **Users:** {len(self.bot.users)}"
                      f"\n> **Servers:** {len(self.bot.guilds)}"
        	      f"\n> **Uptime:** {days}**d** {hours}**h** {minutes}**m** {seconds}**s**",
                inline=False
            )
            e.add_field(
                name="✧ __Credits__",
                value=f"> **Dev:** `gamingderp`",
                inline=False
            )
            e.add_field(
                name="✧ __Links__",
                value=f"<:Discord:1146086582399541329> [Join SDA!](https://discord.gg/v4WAvEYe2Z)"
                      f"\n<:GitHub:1146086606537773167> [Repo Link](https://github.com/GamingDerp/ArchiveBot)"
                      f"\n:link: [Add ArchiveBot!](https://discord.com/api/oauth2/authorize?client_id=1143360299534143640&permissions=414464724032&scope=bot)"
                      f"\n:coin: [Tip ArchiveBot!](https://linktr.ee/StoneworksDiscordArchive)",
                inline=False
            )
            e.set_footer(text=f"Requested by {interaction.user.name}")
            e.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=e, ephemeral=True)
        except Exception as e:
            print(e)        

async def setup(bot):
    await bot.add_cog(CommandCog(bot))
