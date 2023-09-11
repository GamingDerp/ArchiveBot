import os
import re
import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import datetime, timedelta
import time
import asyncio

# Stores when the 
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.launch_time = datetime.utcnow()

# Server Commands Embed
se = discord.Embed(color=0x0E0E0E)
se.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
se.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
se.add_field(
    name="🔍 __Server Commands__",
    value=f"> `Search`, `Random`",
)

# General Commands Embed
ge = discord.Embed(color=0x0E0E0E)
ge.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
ge.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
ge.add_field(
    name="📌 __General Commands__",
    value=f"> `Help`, `Info`, `Test`, `Ping`",
)

# Fun Commands Embed
fe = discord.Embed(color=0x0E0E0E)
fe.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
fe.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
fe.add_field(
    name="🎉 __Fun Commands__",
    value=f"> `Coinflip`, `Lovetest`",
)

# Misc Commands Embed
me = discord.Embed(color=0x0E0E0E)
me.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
me.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
me.add_field(
    name="🧮 __Misc Commands__",
    value=f"> `Whois`, `ESteal`",
)

# Help Menu Dropdown
class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Server Commands", description="Search, Random", emoji="🔍"),
            discord.SelectOption(label="General Commands",description="Help, Info, Test, Ping", emoji="📌"),
            discord.SelectOption(label="Fun Commands", description="Coinflip, Lovetest", emoji="🎉"),
            discord.SelectOption(label="Misc Commands", description="Whois, ESteal", emoji="🧮"),
        ]
        super().__init__(min_values=1, max_values=1, options=options)

    async def callback(self, interaction:discord.Interaction):
        if self.values[0] == "Server Commands":
            await interaction.response.edit_message(embed=se)
        if self.values[0] == "General Commands":
            await interaction.response.edit_message(embed=ge)
        if self.values[0] == "Fun Commands":
            await interaction.response.edit_message(embed=fe)
        if self.values[0] == "Misc Commands":
            await interaction.response.edit_message(embed=me) 
    
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
        bot_id = 1143360299534143640
        if str(bot_id) in message.content:
            await message.channel.send("I've been summoned! If you need me do `!help` <:CatWave:1123898399557693470>")
    
    @commands.Cog.listener()
    async def on_ready(self):
            await self.bot.tree.sync()
    
    # Test command
    @bot.tree.command(description="Sends a message if the bot is online")
    async def test(self, interaction: discord.Interaction):
            await interaction.response.send_message("I'm up and indexing! <a:DerpPet:1143780090979831928>", ephemeral=True)
    
    # Help Command
    @bot.tree.command(description="Sends ArchiveBot's help menu")
    async def help(self, interaction: discord.Interaction):
        e = discord.Embed(color=0x0E0E0E)
        e.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
        e.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
        e.add_field(
            name="✧ __Command Menus__",
            value=f"> 🔍 Server"
                  f"\n> 📌 General"
                  f"\n> 🎉 Fun"
                  f"\n> 🧮 Misc"
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
            e = discord.Embed(color=0x0E0E0E)
            e.set_author(name="Bot Information", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
            e.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
            e.add_field(
                name="✧ __Index__",
                value=f"> **Servers:** {index_server_count}",
                inline=False
            )
            e.add_field(
                name="✧ __Statistics__",
                value=f"> **Commands:** [10]"
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
                value=f"<:Discord:1143769008420692009> [Join SDA!](https://discord.gg/v4WAvEYe2Z)"
                      f"\n<:GitHub:1123773190238392504> [Repo Link](https://github.com/GamingDerp/ArchiveBot)"
                      f"\n:link: [Add ArchiveBot!](https://discord.com/api/oauth2/authorize?client_id=1143360299534143640&permissions=414464724032&scope=bot)",
                inline=False
            )
            e.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            e.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=e, ephemeral=True)
        except Exception as e:
            print(e)
                                 
    # Coinflip Command
    @bot.tree.command(description="Sends heads or tails")
    async def coinflip(self, interaction: discord.Interaction):
        choice = ["Heads", "Tails"]
        await interaction.response.send_message(f"{random.choice(choice)}!")
    
    # Ping Command
    @bot.tree.command(description="Sends your ping")
    async def ping(self, interaction: discord.Interaction):
        e = discord.Embed(color=0x0E0E0E)
        e.add_field(
            name="📶 Ping",
            value=f"Your ping is **{round(self.bot.latency * 1000)}**ms",
    	    inline=False
        )
        await interaction.response.send_message(embed=e, ephemeral=True)
    
    # Love Test Command
    @bot.tree.command(description="Compares the love rate of two users")
    async def lovetest(self, interaction: discord.Interaction, user1:discord.Member, user2:discord.Member):
    
        love_rate = str(random.randrange(0, 100))
        derp_id = 532706491438727169
        oni_id = 700958482454806574
        terra_id = 240233060455546882
        jimmy_id = 318391989198651394
        zuko_id = 173072155498512385
        
        e = discord.Embed(color=0x0E0E0E)
        e.title = "❤️ Love Test"
        
        if user1.id == derp_id and user2.id == oni_id or user1.id == oni_id and user2.id == derp_id:
            e.description = f"**{user1.mention}** and **{user2.mention}** are a **100%** match! :flushed:"
            await interaction.response.send_message(embed=e)
        elif user1.id == derp_id and user2.id != oni_id or user1.id == oni_id and user2.id != derp_id:
            e.description = f"**{user1.mention}** and **{user2.mention}** are a **0%** match! :flushed:"
            await ctx.send(embed=e)
        elif user1.id == jimmy_id and user2.id == zuko_id or user1.id == zuko_id and user2.id == jimmy_id:
            e.description = f"**{user1.mention}** and **{user2.mention}** are a **100%** match! :flushed:"
            await interaction.response.send_message(embed=e)
        else:
            e.description = f"**{user1.mention}** and **{user2.mention}** are a **{love_rate}%** match! :flushed:"
            await interaction.response.send_message(embed=e)
                                 
    # WhoIs Command
    @bot.tree.command(description="Sends information about a users account")
    async def whois(self, interaction: discord.Interaction, user:discord.Member):
        e = discord.Embed(color=0x0E0E0E)
        e.set_author(name=f"Gathering Information..."),
        if user.avatar:
            e.set_thumbnail(url=user.avatar.url)
        e.add_field(name="📍 Mention", value=user.mention)
        e.add_field(name="🔖 ID", value=user.id)
        e.add_field(name="📑 Nickname", value=user.display_name)
        e.add_field(name="📅 Created On", value=user.created_at.strftime("`%B %d, %Y %H:%M %p`"))
        e.add_field(name="📅 Joined On", value=user.joined_at.strftime("`%B %d, %Y %H:%M %p`"))
        if user.premium_since:
            e.add_field(name=f"<a:DiscordBoost:1121298549657829436> Boosting", value=user.premium_since.strftime("`%B %d, %Y %H:%M %p`"))
        e.add_field(name="👑 Top Role", value=user.top_role.mention)
        e.add_field(name="🎲 Activity", value=f"{user.activity.name}" if user.activity is not None else None)
        e.add_field(name="🚦 Status", value=user.status)
        emotes = {
            "hypesquad_brilliance": "<:HypeSquadBrilliance:1123772502024405053>",
            "hypesquad_bravery": "<:HypeSquadBravery:1123772444994437240>",
            "hypesquad_balance": "<:HypeSquadBalance:1123772443069259897>",
            "bug_hunter": "<:BugHunter:1123772432679981057>",
            "bug_hunter_level_2": "<:BugHunterLevel2:1123772435150422086>",
            "early_verified_bot_developer": "<:EarlyVerifiedBotDeveloper:1123772440338776064>",
            "verified_bot_developer": "<:EarlyVerifiedBotDeveloper:1123772440338776064>",
            "active_developer": "<:ActiveDeveloper:1123772429307744287>",
            "hypesquad": "<:HypeSquadEvents:1123772447125155963>",
            "early_supporter": "<:EarlySupporter:1123772438380019762>",
            "discord_certified_moderator": "<:ModeratorProgramsAlumni:1123772518365409370>",
            "staff": "<:Staff:1123772450430267393>",
            "partner": "<:Partner:1123774032932769812>",
        }
        badges = [
            emoji
            for f in user.public_flags.all()
            if (emoji := emotes.get(f.name))
        ]
        if badges:
            e.add_field(name="🧬 Flags", value=" ".join(badges))
        else:
            e.add_field(name="🧬 Flags", value="None")
        e.add_field(name="🤖 Bot?", value=user.bot)
        if user.status != user.mobile_status:
            e.add_field(name="📺 Device", value="Desktop")
        elif user.status != user.desktop_status:
            e.add_field(name="📺 Device", value="Mobile")
        req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            e.add_field(name="📰 Banner", value="**Linked Below**")
            e.set_image(url=banner_url)
        else:
            e.add_field(name="📰 Banner", value="None")
        e.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url),
        e.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=e, ephemeral=True)                               
    
    # Emoji Steal Command
    @bot.tree.command(description="Sends the image file link for a custom emoji")
    async def esteal(self, interaction: discord.Interaction, emoji: str):
        try:
            match = re.match(r"<a?:([a-zA-Z0-9_]+):(\d+)>", emoji)
            if match:
                emoji_name = match.group(1)
                emoji_id = int(match.group(2))
                animated = emoji.startswith("<a:")
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}." + ("gif" if animated else "png")
                await interaction.response.send_message(f":link: {emoji_url}", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid emoji format", ephemeral=True)
        except Exception as e:
            print(e)

    
async def setup(bot):
    await bot.add_cog(CommandCog(bot))
