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
        self.Categories = [840074899447480360, 840052147936165911, 849423703091445840, 1112916591043153980, 969999473189199932, 1223189260895522886]
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
            await asyncio.sleep(86400)

    async def wait(self, message):
        print(message)
        index = 0
        chars = r"-/-\-"
        while True:
            print(f"{message} {chars[index]}")
            index += 1
            if index + 1 == len(chars):
                index = 0
            await asyncio.sleep(0.20)

    async def index_servers(self):
        status = self.bot.loop.create_task(self.wait("Indexing Servers"))
        index = {}
        server_count = 0
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
                            server_count += len(server_data)
                    if category_data:
                        index[category.name.lower()] = category_data
        self.index = index
        status.cancel()
        channel = self.bot.get_channel(1337751646977134704)
        try:
            await channel.edit(name=f"🧾 Servers Indexed: {server_count}")
        except discord.HTTPException as e:
            print(f"Failed to update channel name: {e}")
        print("Successfully Indexed Servers")
    
    @commands.hybrid_command(name="search", description="Search for a server")
    async def search(self, ctx, *, search_term):
        if ctx.prefix == "!" and ctx.invoked_with in ["search"]:
            return
        try:
            search_term = search_term.lower()
            discords = {}
            for channels in self.index.values():
                for channel, servers in channels.items():
                    for server, link in servers.items():
                        if search_term in str(server).lower():
                            discords[server] = link
            if not discords:
                await ctx.interaction.response.send_message("No matching servers found.", ephemeral=True)
                return
            sorted_servers = sorted(discords.keys())
            pages = [sorted_servers[i:i + 10] for i in range(0, len(sorted_servers), 10)]
            current_page = 0
            def generate_page():
                embed = discord.Embed(color=0x0E0E0E)
                embed.set_author(name=f"Servers with '{search_term}' in their name")
                embed.description = "\n".join([f"• [{server}]({discords[server]})" for server in pages[current_page]])
                embed.set_footer(text=f"Page {current_page + 1}/{len(pages)}")
                return embed
            await ctx.interaction.response.send_message(embed=generate_page(), ephemeral=True)
            try:
                message = await ctx.interaction.original_response()
            except Exception as e:
                print(f"Error retrieving original response: {e}")
                message = None
            class SearchButtons(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=60)
                @discord.ui.button(style=discord.ButtonStyle.primary, label="◀️")
                async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    nonlocal current_page
                    if interaction.user is None:
                        await interaction.response.send_message("Error: Interaction user is None.", ephemeral=True)
                        return
                    if interaction.user != ctx.author:
                        return await interaction.response.send_message("You can't control this menu.", ephemeral=True)
                    current_page = (current_page - 1) % len(pages)
                    try:
                        await interaction.response.edit_message(embed=generate_page(), view=self)
                    except Exception as e:
                        print(f"Error editing message: {e}")
                @discord.ui.button(style=discord.ButtonStyle.primary, label="▶️")
                async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    nonlocal current_page
                    if interaction.user is None:
                        await interaction.response.send_message("Error: Interaction user is None.", ephemeral=True)
                        return
                    if interaction.user != ctx.author:
                        return await interaction.response.send_message("You can't control this menu.", ephemeral=True)
                    current_page = (current_page + 1) % len(pages)
                    try:
                        await interaction.response.edit_message(embed=generate_page(), view=self)
                    except Exception as e:
                        print(f"Error editing message: {e}")
            view = SearchButtons()
            await message.edit(embed=generate_page(), view=view)
        except Exception as e:
            print(f"Error in search command: {e}")
    
    @commands.hybrid_command(name="random", description="Sends a random discord link")
    async def random(self, ctx):
        if ctx.prefix == "!" and ctx.invoked_with in ["random"]:
            return
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
