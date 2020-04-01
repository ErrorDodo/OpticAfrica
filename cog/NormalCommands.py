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
from art import *


class NormalCommands(commands.Cog, name="Commands"):
    """Commands"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["user"])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get a users info."""

        if not user:
            user = ctx.message.author
        try:
            playinggame = user.activity.title
        except:
            playinggame = None

        server = ctx.message.guild
        embed = discord.Embed(color=0xDEADBF)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Discriminator", value=user.discriminator)
        embed.add_field(name="Bot", value=str(user.bot))
        embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Animated Avatar", value=str(user.is_avatar_animated()))
        embed.add_field(name="Playing", value=playinggame)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Color", value=str(user.color))

        try:
            roles = [x.name for x in user.roles if x.name != "@everyone"]

            if roles:
                roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                        if x.name != "@everyone"].index)
                roles = ", ".join(roles)
            else:
                roles = "None"
            embed.add_field(name="Roles", value=roles)
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command(aliases=["server"])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """Display Server Info"""
        server = ctx.guild
        verif = server.verification_level

        online = len([m.status for m in server.members
                        if m.status == discord.Status.online or
                        m.status == discord.Status.idle])

        embed = discord.Embed(color=0xDEADBF)
        embed.add_field(name="Name", value=f"**{server.name}**\n({server.id})")
        embed.add_field(name="Owner", value=server.owner)
        embed.add_field(name="Online (Cached)", value=f"**{online}/{server.member_count}**")
        embed.add_field(name="Created at", value=server.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Channels", value=f"Text Channels: **{len(server.text_channels)}**\n"
        f"Voice Channels: **{len(server.voice_channels)}**\n"
        f"Categories: **{len(server.categories)}**\n"
        f"AFK Channel: **{server.afk_channel}**")
        embed.add_field(name="Roles", value=str(len(server.roles)))
        embed.add_field(name="Emojis", value=f"{len(server.emojis)}/100")
        embed.add_field(name="Region", value=str(server.region).title())
        embed.add_field(name="Security", value=f"Verification Level: **{verif}**\n"
        f"Content Filter: **{server.explicit_content_filter}**")

        try:
            embed.set_thumbnail(url=server.icon_url)
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None, format_type: str = None):
        """Get a user's avatar"""
        await ctx.channel.trigger_typing()

        if user is None:
            user = ctx.message.author
        try:
            color = await helpers.get_dominant_color(self.bot, user.avatar_url_as(format="png"))
        except:
            color = 0xDEADBF
        em = discord.Embed(color=color, title="{}'s Avatar".format(user.name))
        if format_type is None or format_type not in ["png", "jpg", "gif", "jpeg", "webp"]:
            await ctx.send(embed=em.set_image(url=user.avatar_url))
        else:
            await ctx.send(embed=em.set_image(url=user.avatar_url_as(format=format_type)))

    @commands.command()
    async def ASCII(self, ctx, *, art: str = None):
        art2 = text2art(art, font='random')
        await ctx.send("```" + art2 + "```")

    @commands.command()
    async def spotify(self, ctx, user: discord.Member=None):
        """Returns spotfiy information"""
        user = user or ctx.author
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(colour=activity.colour, title=activity.name)
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                embed.add_field(name="Song Title", value=activity.title)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.add_field(name="Started Playing", value=activity.start.strftime("%a, %H:%M"))
                embed.add_field(name="Time till next song", value=activity.end.strftime("%a, %H:%M"))
                embed.set_thumbnail(url=activity.album_cover_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def kanye(self, ctx):
        """Posts a Kayne Quote"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.kanye.rest/") as r:
                if r.status == 200:
                    js = await r.json()
                    embed = discord.Embed()
                    embed.add_field(name="Quote:", value=js['quote'])
                    await ctx.send(embed=embed)
                else:
                    print(f"Api seems to be down {r.status}")



    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ How hot are you? """
        user = user or ctx.author


        random.seed(user.id)
        if user.id == 259932683206000651:
            await ctx.send(f"**{user.name}** is **100%** hot 💞")
        
        elif user.id == 260010013756489733:
            await ctx.send(f"**{user.name}** is **110%** hot 💞")

        elif user.id == 215080475377532930:
            await ctx.send(f"**{user.name}** is **169%** hot ;) 💞")

            
        else:
            r = random.randint(1, 100)
            hot = r / 1.17    
            
            emoji = "💔"
            if hot > 25:
                emoji = "❤"
            if hot > 50:
                emoji = "💖"
            if hot > 75:
                emoji = "💞"

            await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")
                    

    @commands.command(aliases=['calc', 'love'])
    async def lovecalc(self, ctx, *, user: discord.Member = None):
        """A love Calc"""
        user = user or ctx.author

        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "💔"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is a **{hot:.2f}%** match for **{ctx.author.name}** {emoji}")

def setup(client):
    client.add_cog(NormalCommands(client))
    print("Normal commands have been loaded")