import os
import asyncio
import time
import re
import traceback
from typing import Optional
import sys
import random
import discord
from discord.ext import commands, tasks

class IndexCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_updated = None
        self.Categories = [840074899447480360, 840052147936165911, 849423703091445840, 1112916591043153980, 969999473189199932]
        self.server_id = self.bot.config["server_id"]
        self.index = {}
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        while True:
            try:
                await self.index_servers()
            except:
                print(traceback.format_exc())
            await asyncio.sleep(3600)

    async def on_command_error(self, context, exception):
        ignored = (commands.CommandNotFound)
        if isinstance(exception, ignored):
            return
        await context.send(embed=discord.Embed(description=str(exception)))
        silent = (
            commands.MissingRequiredArgument,
            commands.CommandOnCooldown,
            commands.BadArgument,
            commands.CheckFailure,
            commands.NoPrivateMessage,
            commands.DisabledCommand
        )
        if not isinstance(exception, silent):
            traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    async def wait(self, message):
        print(message)
        index = 0
        chars = r"-/-\-"
        while True:
            print(f"{message} {chars[index]}")
            index += 1
            if index + 1 == len(chars):
                index = 0
            await asyncio.sleep(0.21)

    async def index_servers(self):
        status = self.bot.loop.create_task(self.wait("Indexing Servers"))
        index = {}
        server = self.bot.get_guild(self.server_id)
        if server:
            for category_id in self.Categories:
                category = discord.utils.get(server.categories, id=category_id)
                if category:
                    category_data = {}
                    for channel in category.text_channels:
                        messages = []
                        async for message in channel.history(limit=None):
                            messages.append(message)
                        server_data = {
                            msg.content.split("\n")[0].replace("__**", "").replace("**__", ""): msg.content.split("\n")[1]
                            for msg in messages
                            if msg.content.count("\n") and msg.content.count("discord.gg")
                        }
                        if server_data:
                            category_data[channel.name.lower()] = server_data
                    if category_data:
                        index[category.name.lower()] = category_data
        self.index = index
        status.cancel()
        print("Successfully Indexed Servers")
    
    # Search Command
    @commands.hybrid_command(name="search", description="Search for a server")
    async def search(self, ctx, *, search_term):
        try:
            search_term = search_term.lower()
            discords = {}
            for channels in self.index.values():
                for channel, servers in channels.items():
                    for server, link in servers.items():
                        if search_term in str(server).lower():
                            discords[server] = link
            if not discords:
                await ctx.send("No matching servers found.", ephemeral=True)
                return
            pages = [list(discords.keys())[i:i + 10] for i in range(0, len(discords), 10)]
            current_page = 0

            def generate_page():
                e = discord.Embed(color=0x0E0E0E)
                e.set_author(name=f"Servers with '{search_term}' in their name")
                e.description = ""
                for server in pages[current_page]:
                    link = discords[server]
                    e.description += f"\n• [{server}]({link})"
                e.set_footer(text=f"Page {current_page + 1}/{len(pages)}")
                return e
            message = await ctx.send(embed=generate_page(), ephemeral=True)

            async def pagination_callback(interaction, direction):
                nonlocal current_page
                if direction == "prev":
                    current_page = (current_page - 1) % len(pages)
                else:
                    current_page = (current_page + 1) % len(pages)         
                await interaction.response.edit_message(embed=generate_page())
       
            prev_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="◀️")
            next_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="▶️")
            prev_button.callback = lambda i: pagination_callback(i, "prev")
            next_button.callback = lambda i: pagination_callback(i, "next")
            view = discord.ui.View()
            view.add_item(prev_button)
            view.add_item(next_button)
            await message.edit(embed=generate_page(), view=view)

            while True:
                try:
                    interaction = await self.bot.wait_for("button_click", timeout=60)
                    if interaction.user == ctx.author and interaction.message.id == message.id:
                        await interaction.callback(interaction)
                except asyncio.TimeoutError:
                    await message.edit(view=None)
                    break
                except Exception as e:
                    print(e)
        except asyncio.TimeoutError:
            await message.edit(view=None)
        except Exception as e:
            print(e)
    
    # Random Command
    @commands.hybrid_command(name="random", description="Sends a random discord link")
    async def random(self, ctx):
        try:
            e = discord.Embed(color=0x0E0E0E)
            e.set_author(name="Random Server")
            selection = []
            for channels in self.index.values():
                for channel, index in channels.items():
                    for server, link in index.items():
                        selection.append([server, link])
            choice = random.choice(selection)
            e.description = f"<:Discord:1143769008420692009> **[{choice[0]}]({choice[1]})**"
            await ctx.send(embed=e, ephemeral=True)
        except Exception as e:
            print(e)
            
    
async def setup(bot):
    await bot.add_cog(IndexCog(bot))
