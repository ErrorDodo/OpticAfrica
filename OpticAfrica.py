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
import os
import sqlite3
from regex import regex as re


import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def gettoken():
    file1 = "token.json"
    with open(file1) as f:
        d = json.load(f)
        oof = d['token']
        client.run(oof)

client = commands.Bot(command_prefix="!!", status=discord.Status.offline)
client.remove_command('help')

@client.event
async def on_ready():
    servers = list(client.guilds)
    print("-----")
    print(f"{client.user.name} is Connected on {str(len(servers))} server(s):")
    print("-----")
    print("Bot created by Dodo#5337")
    print("-----")
    await asyncio.sleep(0.2)
    print('\n'.join(server.name for server in servers))
    print("-----")
    for filename in os.listdir('./cog'):
        if filename.endswith('.py'):
            client.load_extension(f'cog.{filename[:-3]}')
    await asyncio.sleep(2)
    await client.change_presence(status=discord.Status.offline, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(set(client.get_all_members()))} Users | !!sadcat '))

@client.event
async def on_message(message):
    if not message.guild:
        return 
    elif  message.author.guild_permissions.manage_messages:
        return 
    elif "https://discord.gg" in message.content:
        await message.delete()
    elif "discord.gg" in message.content:
        await message.delete()
    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    message = after
    if not message.guild:
        return 
    elif  message.author.guild_permissions.manage_messages:
        return 
    elif "https://discord.gg" in message.content:
        await message.delete()         
    elif "discord.gg" in message.content:
        await message.delete()

    await client.process_commands(message)
                

@client.command()
async def shutdown(ctx):
    if ctx.author.id == 259932683206000651:
        await ctx.send("Bot is shutting down")
        await client.logout()

gettoken()


