import logging
import sys
import os
import aiohttp
import traceback
import discord
from discord.ext import commands
from profanity import profanity
import sqlite3


db = sqlite3.connect('main.sqlite', check_same_thread=False)
cursor = db.cursor()
CURSES = ("nigger", "nigga", "dick", "cunt", "anal", "blowjob", "blow job", "dyke", "fag", "faggot", "jizz", "nig", "wank", "whore", "slut", "retard", "retarded", "bitch")



class automod:
    async def check_curses(self, message):
        if any([curse in message.content.lower() for curse in CURSES]):
            await message.delete()
            await message.author.send(f"{message.author.mention} don't use that type of language")
            return True
        return False

class Filter(commands.Cog, name="Filter"):
    """Filtering"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.author.send(f"{message.author.mention} don't use that type of language")
            return 
        elif not await automod.check_curses(self, message):
            return 
        await self.client.process_commands(message)
        

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        message = after
        if profanity.contains_profanity(message.content):
            await message.delete()
            await message.author.send(f"{message.author.mention} don't use that type of language")
            return
        elif not await automod.check_curses(self, message):
            return

        await self.client.process_commands(message)


def setup(client):
    client.add_cog(Filter(client))
    print("Filtering has been loaded") 










