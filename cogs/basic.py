import discord
import time
import asyncio
import datetime
import traceback
import logging
from discord.ext import commands

class basic(commands.Cog, name='basic'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Checks the bot is running"""
        fren = ctx.message.author.mention
        await ctx.send(f"{fren} Hey fren!")

    @commands.command()
    async def ping(self, ctx):
        """Returns the amount of latency from the host to the Discord WS/REST API"""
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x666666)
        embed.add_field(name="Pong Recieved!", value="Calculating...")
        resp = await ctx.send(embed=embed)
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x666666)
        diff = resp.created_at - ctx.message.created_at
        embed.add_field(name="Ping", value=f'**{1000*diff.total_seconds():.1f}** ms')
        embed.add_field(name='WS', value=f'**{round(self.bot.latency*1000, 2)}** ms')
        embed.set_author(icon_url=ctx.me.avatar_url, name=ctx.me)
        embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        await resp.edit(embed=embed)


def setup(bot):
    bot.add_cog(basic(bot))
