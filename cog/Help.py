import discord
import random
from discord.ext import commands, tasks
from discord import Spotify
import asyncio
from discord import Streaming
import aiohttp
import time
from sys import stdout
import json
import io
import typing



class Helper(commands.Cog, name="Help"):

    """Help Formatter"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed = discord.Embed(title=f"Error in {ctx.command}", description=f"`{ctx.command.qualifed_name} {ctx.command.signature}` \n{error}", colour=0x43788)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"Error in {ctx.command}", description=f"{error}", colour=0x43788)
            await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *cog):
        """Gets all cogs and commands"""

        if not cog:

            embed = discord.Embed(colour=0x437840)

            cog_desc = ""
            for x in self.client.cogs:
                cog_desc += ("**{}** - {}".format(x,self.client.cogs[x].__doc__) + '\n')
            embed.add_field(name="Cogs", value=cog_desc[0:len(cog_desc)-1], inline=False)
            embed.set_footer(text="Use a word you see to dive deeper into the help. E.g !!help Commands")
            await ctx.message.add_reaction(emoji="👀")
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed= discord.Embed(title='Error', description="That is way too many cogs", colour = 0x437840)
                await ctx.message.author.send('', embed=embed)
            else:
                found = False
                for x in self.client.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(colour = 0x437840)
                            scog_info = ""
                            for c in self.client.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f"**{c.name}** - {c.help}\n"
                            embed.add_field(name=f"{cog[0]} Module - {self.client.cogs[cog[0]].__doc__}", value=scog_info)
                            found = True
                if not found:
                    for x in self.client.cogs:
                        for c in self.client.get_cog(x).get_commands():
                            if c.name == cog[0]:
                                embed = discord.Embed(colour = 0x437840)
                                embed.add_field(name=f"{c.name} - {c.help}", value=f"Proper Syntax:\n`{c.qualified_name} {c.signature}`")
                        found = True
                    if not found:
                        embed = discord.Embed(title="Error!",description='How do you even use "'+cog[0]+ '"?' ,colour = 0x437840)
                else:
                    await ctx.message.add_reaction(emoji="👀")
                await ctx.send(embed=embed)

"""    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed = discord.Embed(title=f'Error in {ctx.command}', description=f'`{ctx.command.qualifed_name} {ctx.command.signature}`\n{error}', colour=0x43740)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f'Error in {ctx.command}', description=f'{error}', colour=0x43740)
            await ctx.send(embed=embed)"""
          





def setup(client):
    client.add_cog(Helper(client))
    print("Helping commands have been loaded")