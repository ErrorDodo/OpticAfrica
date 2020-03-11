import discord
import random
from discord.ext import commands, tasks
from discord import Spotify
import asyncio
import aiohttp
import time
from sys import stdout
import json
import io


class UWUCommands(commands.Cog, name="Uwu"):
    """Just some random anime stuff"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cuddle"])
    async def hug(self, ctx, user: discord.Member = None):
        """Hugs a user"""
        user = user or ctx.author
        ted = ['hug', 'cuddle']    
        fish = random.choice(ted)      
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://purrbot.site/api/img/sfw/{fish}/gif") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(color=0xDEADBF)
                    embed.set_author(name=f"{ctx.author.name} hugs {user.name}")
                    embed.set_image(url=js['link'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api seems to be down {r.status}")

    @commands.command()
    async def poke(self, ctx, user: discord.Member = None):
        """Pokes a user"""
        user = user or ctx.author          
        async with aiohttp.ClientSession() as session:
            async with session.get("https://purrbot.site/api/img/sfw/poke/gif") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(color=0xDEADBF)
                    embed.set_author(name=f"{ctx.author.name} pokes {user.name}")
                    embed.set_image(url=js['link'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api seems to be down {r.status}")

    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        """Slaps a user"""
        user = user or ctx.author          
        async with aiohttp.ClientSession() as session:
            async with session.get("https://purrbot.site/api/img/sfw/slap/gif") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(color=0xDEADBF)
                    embed.set_author(name=f"{ctx.author.name} has slapped {user.name}")
                    embed.set_image(url=js['link'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api seems to be down {r.status}")


    @commands.command(aliases=['noticemesenpai'])
    async def noticeme(self, ctx):
        """Notice me"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://i.alexflipnote.dev/500ce4.gif") as resp:
                if resp.status != 200:
                    return print("Could not download file....")
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'noticeme.gif'))

    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        """Pats a user"""
        user = user or ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.life/api/v2/img/pat") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed(color=0xDEADBF)
                    embed.set_author(name=f"{ctx.author.name} gives pats to {user.name}")
                    embed.set_image(url=js['url'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api seems to be down {r.status}")



def setup(client):
    client.add_cog(UWUCommands(client))
    print("UwuCommands have been loaded!")

        