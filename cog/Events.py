import logging
import sys
import os
import aiohttp
import traceback
import discord
from discord.ext import commands




class Events(commands.Cog):
    """Events."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return await self.client.process_commands(message)
   
        if message.author.guild_permissions.manage_messages:
            return 

        elif "https://discord.gg" in message.content:
            await message.delete()
            
            try:
                await message.author.send("Don't post discord invite links")
                
            except discord.Forbidden:
                await message.channel.send("Don't post discord invite links.")
                
        
        elif "discord.gg" in message.content:
            await message.delete()
            
            try:
                await message.author.send("Don't post discord invite links")
                
            except discord.Forbidden:
                await message.channel.send("Don't post discord invite links")
        await self.client.process_commands(message)
                
        

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        message = after
        if not message.guild:
            return 
        
        if message.author.guild_permissions.manage_messages:
            return 

        elif "https://discord.gg" in message.content:
            await message.delete()
            
            try:
                await message.author.send("Don't post discord invite links")
                
            except discord.Forbidden:
                await message.channel.send("Don't post discord invite links.")
                
        
        elif "discord.gg" in message.content:
            await message.delete()
            
            try:
                await message.author.send("Don't post discord invite links")
                
            except discord.Forbidden:
                await message.channel.send("Don't post discord invite links")
                
        await self.client.process_commands(message)


def setup(client):
    client.add_cog(Events(client))
    print("Events have been loaded")