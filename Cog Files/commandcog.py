import os
import discord
import random
from discord.ext import commands
from datetime import datetime, timedelta
import time
import asyncio

# Stores when the bot was started
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
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
    value=f"> `Help`, `Info`, `Test`, `Ping`, `/Poll`",
)

# Fun Commands Embed
fe = discord.Embed(color=0x0E0E0E)
fe.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
fe.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
fe.add_field(
    name="🎉 __Fun Commands__",
    value=f"> `Coinflip`, `Ask`, `Reverse`, `Say`, `Lovetest`",
)

# Misc Commands Embed
me = discord.Embed(color=0x0E0E0E)
me.set_author(name="Bot Commands", icon_url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
me.set_thumbnail(url="https://media.discordapp.net/attachments/807071768258805764/1143728544971763742/sdalogo.jpg")
me.add_field(
    name="🧮 __Misc Commands__",
    value=f"> `Whois`, `Snipe`, `Remind`, `ESteal`",
)

# Help Menu Dropdown
class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Server Commands", description="Search, Random", emoji="🔍"),
            discord.SelectOption(label="General Commands",description="Help, Info, Test, Ping, /Poll", emoji="📌"),
            discord.SelectOption(label="Fun Commands", description="Coinflip, Ask, Reverse, Say, Lovetest", emoji="🎉"),
            discord.SelectOption(label="Misc Commands", description="Whois, Snipe, Remind, ESteal", emoji="🧮"),
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
    
    # Test command
    @commands.command()
    async def test(self, ctx):
        await ctx.send("I'm up and indexing! <a:DerpPet:1143780090979831928>")
    
    # Help Command
    @commands.command()
    async def help(self, ctx):
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
        await ctx.send(embed=e, view=view)
    
    # Info Command
    @commands.command()
    async def info(self, ctx):
        try:
            index_cog = self.bot.get_cog('IndexCog')
            if index_cog:
                index_server_count = sum(sum(len(links) for links in section.values()) for section in index_cog.index.values())
            else:
                index_server_count = 0
            total_lines = 29
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
                value=f"> **Commands:** [17]"
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
                value=f"<:GitHub:1123773190238392504> [Repo Link](https://github.com/GamingDerp/SleeplessNightsBot)"
                      f"\n:link: [Add ArchiveBot!](https://discord.com/api/oauth2/authorize?client_id=1143360299534143640&permissions=414464735297&scope=bot)",
                inline=False
            )
            e.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            e.timestamp = datetime.utcnow()
            await ctx.send(embed=e)
        except Exception as e:
            print(e)
                                 
    # Coinflip Command
    @commands.command()
    async def coinflip(self, ctx):
        choice = ["Heads", "Tails"]
        await ctx.send(f"{random.choice(choice)}!")

    # Ask Command
    @commands.command()
    async def ask(self, ctx):
        choice = ["Yes", "No", "Obviously", "Wtf??", "I'm not sure..", "Maybe...?", "Stop asking.", "Find out for yourself, smh", "Crabs", "Ask Derp :eyes:"]
        await ctx.send(f"{random.choice(choice)}")

    # Reverse Command
    @commands.command()
    async def reverse(self, ctx, *, arg="reverse"):
        await ctx.send(arg[::-1])

    # Say Command
    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.send(arg)
        await ctx.message.delete()
    
    # Ping Command
    @commands.command()
    async def ping(self, ctx):
        e = discord.Embed(color=0x0E0E0E)
        e.add_field(
            name="📶 Ping",
            value=f"Your ping is **{round(self.bot.latency * 1000)}**ms",
    	    inline=False
        )
        await ctx.send(embed=e)
    
    # Love Test Command
    @commands.command()
    async def lovetest(self, ctx, user1:discord.Member, user2:discord.Member):
    
        love_rate = str(random.randrange(0, 100))
        derp_id = 532706491438727169
        oni_id = 700958482454806574
    
        if user1.id == derp_id and user2.id == oni_id or user1.id == oni_id and user2.id == derp_id:
            e = discord.Embed(color=0x0E0E0E)
            e.add_field(
                name="❤️ Love Test",
                value=f"**{user1.mention}** and **{user2.mention}** are a **100%** match! :flushed:",
                inline=False
            )
            await ctx.send(embed=e)
        else:
            e = discord.Embed(color=0x0E0E0E)
            e.add_field(
                name="❤️ Love Test",
                value=f"**{user1.mention}** and **{user2.mention}** are a **{love_rate}%** match! :flushed:",
                inline=False
            )
            await ctx.send(embed=e)                             
                                 
    # WhoIs Command
    @commands.command()
    async def whois(self, ctx, user:discord.Member):
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
        e.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url),
        e.timestamp = datetime.utcnow()
        await ctx.send(embed=e)
                                  
    # Snipe Events
    sniped_message = None
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        global sniped_message
        sniped_message = message
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: 
            return
        global sniped_message
        sniped_message = before
        
    # Snipe Command
    @commands.command()
    async def snipe(self, ctx):
        global sniped_message
        if sniped_message is None:
            await ctx.send("There are no recently deleted messages to snipe.")
            return
        if sniped_message.content:
            e = discord.Embed(color=0x0E0E0E)
            e.set_author(name=sniped_message.author.name, icon_url=sniped_message.author.avatar.url)
            e.description = f"> {sniped_message.content}"
            await ctx.send(embed=e)
        elif sniped_message.attachments:
            attachment_url = sniped_message.attachments[0].url
            e = discord.Embed(color=0x0E0E0E)
            e.set_author(name=sniped_message.author.name, icon_url=sniped_message.author.avatar.url)
            e.set_image(url=attachment_url)
            await ctx.send(embed=e)
        sniped_message = None  # Reset sniped message after displaying                                 
                                 
    # Remind Command
    @commands.command()
    async def remind(self, ctx, time, *, task):
        try:
            def convert(time):
                pos = ['s', 'm', 'h', 'd']
                time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
                unit = time[-1]
                if unit not in pos:
                    return -1
                try:
                    val = int(time[:-1])
                except:
                    return -2
                return val * time_dict[unit]
            converted_time = convert(time)
            if converted_time == -1:
                await ctx.send("You didn't input the time correctly!")
                return
            if converted_time == -2:
                await ctx.send("The time must be an integer!")
                return
        
            # Timer Embed
            e = discord.Embed(color=0x0E0E0E)
            e.description = "⏰ Started Reminder ⏰"
            e.add_field(name="Time", value=time)
            e.add_field(name="Task", value=task)
            e.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            e.timestamp = datetime.utcnow()
            await ctx.send(embed=e)
        
            # End Timer Embed
            await asyncio.sleep(converted_time)
            await ctx.send(ctx.author.mention)
            e = discord.Embed(color=0x0E0E0E)
            e.description = "⏰ Time's Up ⏰"
            e.add_field(name="Task", value=task)
            await ctx.send(embed=e)
        except Exception as e:
            print(e)
                                     
    # Emoji Steal Command
    @commands.command()
    async def esteal(self, ctx, emoji: discord.PartialEmoji):
        if emoji.id:
            emoji_url = emoji.url
            await ctx.send(f":link: {emoji_url}")
        else:
            await ctx.send("Please provide a custom emoji.")
    
    # Poll Command - Slash
    @commands.hybrid_command(name="poll", description="Create a poll!")
    async def poll(self, ctx, question:str, option1:str=None, option2:str=None, option3:str=None, option4:str=None, option5:str=None):
        options = [option1, option2, option3, option4, option5]
        options = [option for option in options if option is not None]
        emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]      
        if not options:
            await ctx.send("Please provide at least two options for the poll.")
            return
        if len(options) > 5:
            await ctx.send("You can only have up to 5 options in the poll.")
            return       
        e = discord.Embed(color=0x0E0E0E)
        e.title = f"📊 **{question}**"
        description_text = ""
        for i, option in enumerate(options):
            description_text += f"\n{emoji_list[i]} {option}"
        e.description = description_text
        msg = await ctx.send(embed=e)
        for i in range(len(options)):
            await msg.add_reaction(emoji_list[i])
    
    # Servers Command
    @commands.command()
    async def servers(self, ctx):
        derp_id = 532706491438727169
        
        def generate_page(page):
            page_guilds = pages[page]
            guild_list = "\n".join(f"• {guild.name}" for guild in page_guilds)
            return guild_list

        try:
            if ctx.author.id == derp_id:
                e = discord.Embed(color=0x0E0E0E)
                e.set_author(name="Servers", icon_url=ctx.author.avatar.url)

                if not self.bot.is_ready():
                    await ctx.send("Bot is not ready yet.")
                    return

                pages = [list(self.bot.guilds)[i:i + 10] for i in range(0, len(self.bot.guilds), 10)]

                if not pages:
                    await ctx.send("The bot is not in any servers.")
                    return

                current_page = 0
                guild_list = generate_page(current_page)
                e.description = guild_list
                message = await ctx.send(embed=e)

                await message.add_reaction("◀️")
                await message.add_reaction("▶️")

                def check(reaction, user):
                    return user == ctx.author and reaction.message.id == message.id

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                        if reaction.emoji == "◀️":
                            current_page = (current_page - 1) % len(pages)
                        elif reaction.emoji == "▶️":
                            current_page = (current_page + 1) % len(pages)
                        guild_list = generate_page(current_page)
                        e.description = guild_list
                        await message.edit(embed=e)
                        await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
            else:
                return
        except Exception as e:
            print(e)
            
    
async def setup(bot):
    await bot.add_cog(CommandCog(bot))
