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
        
class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bot.tree.command(description="Sends ArchiveBot's help menu")
    async def help(self, interaction: discord.Interaction):
        e = discord.Embed(color=sda_color)
        e.set_author(name="ArchiveBot Help Menu", icon_url=sda_logo)
        e.set_thumbnail(url=sda_logo)
        e.description = f"> ⚖️ `/Help` - *Sends the* ***ArchiveBot*** *Help Menu* \n> 📌 `/Info` - *Sends information about* ***ArchiveBot*** \n> 🔍 `/Search` - *Search for a specific server* \n> 🎲 `/Random` - *Sends a random server*"
        await interaction.response.send_message(embed=e, ephemeral=True)
    
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
	        total_users = sum(guild.member_count for guild in self.bot.guilds)
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
                value=f"> **Commands:** [4]"
	                  f"\n> **Code:** {total_lines} Lines"
                      f"\n> **Ping:** {round(self.bot.latency * 1000)}ms"
                      f"\n> **Users:** {total_users}"
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
