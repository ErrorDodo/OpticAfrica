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
import sqlite3
import datetime
from discord.utils import get


class WelcomeHelp(commands.Cog, name="Welcome"):
    """Helps with setting up Welcome messages"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(colour=0x95efcc, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.client.get_channel(id=int(result[0]))
            await channel.send(embed=embed)

        cursor.execute(f"SELECT role FROM main WHERE guild_id = {member.guild.id}")
        results = cursor.fetchone()
        if results is None:
            return
        else:
            cursor.execute(f"SELECT role FROM main WHERE guild_id = {member.guild.id}")
            results1 = cursor.fetchone()
            roles = results1[0]
            pineapple = get(member.guild.roles, name=roles)
            await member.add_roles(pineapple)
            

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def welcome(self, ctx):
        """The start of the welcome command"""
        await ctx.send("Available Setup Commands: \nwelcome channel <#channel>\nwelcome text <message>\nrole <@role>")

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def role(self, ctx, role:discord.Role = None):
        """Auto role"""
        role = role.name
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(guild_id, role) VALUES(?,?")
            val = (ctx.guild.id, role)
            await ctx.send(f"Auto role has been set to `{role}`")
        elif result is not None:
            sql = ("UPDATE main SET role = ? WHERE guild_id = ?")
            val = (role, ctx.guild.id)
            await ctx.send(f"Auto role has been updated to `{role}`")
        cursor.execute(sql, val)
        db.commit()

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        """Assign a channel to welcome new users"""
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
            val = (ctx.guild.id, channel.id)
            await ctx.send(f"Channel has been set to `{channel.name}`")
        elif result is not None:
            sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            await ctx.send(f"Channel has been updated to `{channel.name}`")                
        cursor.execute(sql, val)
        db.commit()

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def text(self, ctx, *, text):
        """Assign some text to greet new users"""
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?)")
            val = (ctx.guild.id, text)
            await ctx.send(f"Message has been set to `{text}`")
        elif result is not None:
            sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            await ctx.send(f"Message has been updated to `{text}`")                
        cursor.execute(sql, val)
        db.commit()






def setup(client):
    client.add_cog(WelcomeHelp(client))
    print("Welcome Helper has been loaded")