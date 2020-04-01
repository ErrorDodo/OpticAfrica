import discord
import random
from discord.ext import commands, tasks
from discord.ext.commands import Greedy
from discord import Spotify, Member, TextChannel, VoiceChannel, Webhook, AsyncWebhookAdapter
import asyncio
import aiohttp
import time
from sys import stdout
import json
import io
import typing
import logging
import datetime
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from .utils import checks



db = sqlite3.connect('main.sqlite', check_same_thread=False)
cursor = db.cursor()
Scheduler = AsyncIOScheduler()





class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            raise commands.BadArgument("You cannot punish other staff members")
                                          


class Mod(commands.Cog, name="Mod"):

    """List of mod commands"""

    def __init__(self, client):
        self.client = client
        self.raidmode = {}
        


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(
            self, ctx, amount: int, *, word: typing.Union[discord.Member, str] = None, user: discord.Member = None):
        """Purges text channels"""
        if isinstance(word, discord.Member) and user is None:
            await ctx.channel.purge(limit=amount + 1, check=lambda e: e.author == word)
            await ctx.send(f"Purged {amount} messages from **{word}**.", delete_after=15)
            return

        if isinstance(word, str) and user:
            await ctx.channel.purge(limit=amount + 1, check=lambda e: e.author == user and word in e.content.lower())
            await ctx.send(f"Purged {amount} messages that contained **{word}** from **{user}**.", delete_after=15)
            return

        if isinstance(word, str) and user is None:
            await ctx.channel.purge(limit=amount + 1, check=lambda e: word in e.content.lower())
            await ctx.send(f"Purged {amount} messages that contained **{word}**.", delete_after=15)
            return

        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Purged {amount} messages.", delete_after=15)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """Kicks a member"""
        if user.guild_permissions.manage_messages:
            await ctx.send("I cannot kick moderators/admins")
        elif user.id == 259932683206000651:
            await ctx.send("I cannot ban that person")
        else:
            if reason is None:
                try:
                    await user.send(f'You were kicked from {discord.utils.escape_mentions(discord.utils.escape_markdown(ctx.guild.name))} for `{reason}`')
                    nodm = False
                except discord.HTTPException:
                    nodm = True
                await ctx.guild.kick(user=user, reason="No reason specified")
                embed = discord.Embed(colour= discord.Colour.red(), timestamp= datetime.datetime.utcnow())
                embed.set_author(name=f"Kick | {user}", icon_url=str(user.avatar_url_as(static_format='png', size=2048)))
                embed.add_field(name="User", value=f"{user}({user.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                if nodm:
                    embed.add_field(name="DM Received?", value="No, user has DMs off or has blocked me", inline=False)
                embed.set_footer(text=f"User ID: {user.id} | Mod ID: {ctx.author.id}")
                try:
                    await ctx.send(embed=embed)
                except Exception:
                    pass     
            else:
                try:
                    await user.send(f'You were kicked from {discord.utils.escape_mentions(discord.utils.escape_markdown(ctx.guild.name))} for `{reason}`')
                    nodm = False
                except discord.HTTPException:
                    nodm = True
                await ctx.guild.kick(user=user, reason=reason)
                embed = discord.Embed(colour= discord.Colour.red(), timestamp= datetime.datetime.utcnow())
                embed.set_author(name=f"Kick | {user}", icon_url=str(user.avatar_url_as(static_format='png', size=2048)))
                embed.add_field(name="User", value=f"{user}({user.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                if nodm:
                    embed.add_field(name="DM Received?", value="No, user has DMs off or has blocked me", inline=False)
                embed.set_footer(text=f"User ID: {user.id} | Mod ID: {ctx.author.id}")
                try:
                    await ctx.send(embed=embed)
                except Exception:
                    pass  

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """Bans a member and logs it to a db"""
        if user.id == 259932683206000651:
            await ctx.send("I cannot ban that person")
        elif user.guild_permissions.manage_messages:
            await ctx.send("I cannot ban admins/moderators")    
        else: 
            cursor.execute(f"SELECT member_id FROM bans WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT into bans(guild_id, member_id) VALUES(?,?)")
                val = (ctx.guild.id, user.id)
                cursor.execute(sql, val)
            db.commit()
            if reason is None:
                try:
                    await user.send(f'You were banned from {discord.utils.escape_mentions(discord.utils.escape_markdown(ctx.guild.name))} for `{reason}`')
                    nodm = False
                except discord.HTTPException:
                    nodm = True
                await ctx.guild.ban(user=user, reason="No reason specified")
                embed = discord.Embed(colour= discord.Colour.red(), timestamp= datetime.datetime.utcnow())
                embed.set_author(name=f"Ban | {user}", icon_url=str(user.avatar_url_as(static_format='png', size=2048)))
                embed.add_field(name="User", value=f"{user}({user.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                if nodm:
                    embed.add_field(name="DM Received?", value="No, user has DMs off or has blocked me", inline=False)
                embed.set_footer(text=f"User ID: {user.id} | Mod ID: {ctx.author.id}")

                try:
                    await ctx.send(embed=embed)
                except Exception:
                    pass     
            else:
                try:
                    await user.send(f'You were banned from {discord.utils.escape_mentions(discord.utils.escape_markdown(ctx.guild.name))} for `{reason}`')
                    nodm = False
                except discord.HTTPException:
                    nodm = True
                await ctx.guild.ban(user=user, reason=reason)
                embed = discord.Embed(colour= discord.Colour.red(), timestamp= datetime.datetime.utcnow())
                embed.set_author(name=f"Ban | {user}", icon_url=str(user.avatar_url_as(static_format='png', size=2048)))
                embed.add_field(name="User", value=f"{user}({user.id})", inline=False)
                embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                if nodm:
                    embed.add_field(name="DM Received?", value="No, user has DMs off or has blocked me", inline=False)
                embed.set_footer(text=f"User ID: {user.id} | Mod ID: {ctx.author.id}")
                try:
                    await ctx.send(embed=embed)
                except Exception:
                    pass        

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def move(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        """Move a member to a vc"""
        await ctx.send(f"Moving {ctx.author.mention} to {channel}")
        await member.move_to(channel)

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.has_permissions(manage_messages=True)
    async def antiraid(self, ctx):
        """Checks if anti-raid mode is enabled"""
        if self.raidmode is not None:
            if self.raidmode[ctx.guild.id] is True:
                await ctx.send("Anti-raid mode is enabled.")

        await ctx.send("Anti-raid mode is disabled.")
    
    @antiraid.command()
    @commands.has_permissions(manage_messages=True)
    async def on(self, ctx):
        """Turns on anti-raid mode"""
        for c in ctx.guild.text_channels:
            try:
                await c.edit(slowmode_delay=120)
            except discord.Forbidden:
                pass

        await ctx.send("Slowmode has been enabled on all channels.")
        self.raidmode[ctx.guild.id] = True
    
    @antiraid.command()
    @commands.has_permissions(manage_messages=True)
    async def off(self, ctx):
        """Turns off anti-raid mode"""
        if self.raidmode[ctx.guild.id] is True:
            for c in ctx.guild.text_channels:
                try:
                    await c.edit(slowmode_delay=0)
                except discord.Forbidden:
                    pass

            await ctx.send("Slowmode has been disabled on all channels.")
            self.raidmode[ctx.guild.id] = False
        else:
            await ctx.send("Anti-raid mode is already disabled.")

    @commands.group(case_insensitive=True, invoke_without_command=True, hidden=True)
    @checks.is_admin()
    async def imitate(self, ctx, user: discord.Member, *, text):
        """Use webhooks to imitate a user."""
        await ctx.message.delete()
        url = "https://discordapp.com/api/webhooks/687220234624434183/CZwcDWB0IzPVkRTCNqGfgdIz95ZTz89gy6eEEJk5oRUU51b4ZYzlxaof05xmHCgR8BU8"

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(text, username=str(user.display_name), avatar_url=user.avatar_url)

    @imitate.command()
    @checks.is_admin()
    async def random(self, ctx, *, text):
        """Imitate a random person."""

        await ctx.message.delete()
        user = random.choice([x for x in ctx.guild.members if not x.bot])
        url = "https://discordapp.com/api/webhooks/687220234624434183/CZwcDWB0IzPVkRTCNqGfgdIz95ZTz89gy6eEEJk5oRUU51b4ZYzlxaof05xmHCgR8BU8"

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(text, username=user.display_name, avatar_url=user.avatar_url)

    @imitate.command(hidden=True)
    @checks.is_admin()
    async def custom(self, ctx, user: int, *, text):
        """Imitate a person outside the server"""

        await ctx.message.delete()
        user = await self.bot.get_user_info(user)
        url = "https://discordapp.com/api/webhooks/687220234624434183/CZwcDWB0IzPVkRTCNqGfgdIz95ZTz89gy6eEEJk5oRUU51b4ZYzlxaof05xmHCgR8BU8"

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(text, username=user.display_name, avatar_url=user.avatar_url)

          
    @commands.command()
    @checks.is_admin()
    @commands.has_permissions(manage_messages=True)
    async def block(self, ctx, user: Sinner=None):
        """Blocks a user from chatting in current channel"""
        await ctx.channel.set_permissions(user, send_messages=False)

    @commands.command()
    @checks.is_admin()
    @commands.has_permissions(manage_messages=True)
    async def unblock(self, ctx, user: Sinner=None):
        """Unblocks a user from current channel"""
        await ctx.channel.set_permissions(user, send_messages=True)


def setup(client):
    client.add_cog(Mod(client))
    print("Moderation has been loaded")        