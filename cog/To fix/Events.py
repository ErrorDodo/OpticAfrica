import logging
import sys
import os
import aiohttp
import traceback
import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='Event.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Events(commands.Cog):
    """Events."""

    def __init__(self, client):
        self.client = client




                
        




def setup(client):
    client.add_cog(Events(client))
    print("Events have been loaded")