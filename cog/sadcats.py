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


class sadcats(commands.Cog, name="Sadcat"):
    """Want some sadcats?"""
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def sadcat(self, ctx):
        """Posts a sad cat"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.alexflipnote.dev/sadcat') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js['file'])
                    await ctx.send(embed=embed)
                    #await ctx.send(js['file'])
                else:
                    print(f"Api seems to be down {r.status}")
                    await ctx.send(f"API didn't respond with the value of 200, it instead responded with {r.status}")

    @commands.command()
    async def doggo(self, ctx):
        """Posts a dog"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.alexflipnote.dev/dogs') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js['file'])
                    await ctx.send(embed=embed)
                    #await ctx.send(js['file'])
                else:
                    print(f"Api seems to be down {r.status}")
                    await ctx.send(f"API didn't respond with the value of 200, it instead responded with {r.status}")

    @commands.command()
    async def bird(self, ctx):
        """Posts a bird"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.alexflipnote.dev/birb') as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=js['file'])
                    await ctx.send(embed=embed)
                    #await ctx.send(js['file'])
                else:
                    print(f"Api seems to be down {r.status}")
                    await ctx.send(f"API didn't respond with the value of 200, it instead responded with {r.status}")


def setup(client):
    client.add_cog(sadcats(client))
    print("Sad cats have been loaded")