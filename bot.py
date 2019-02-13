!/usr/bin/env python3
import asyncio
import datetime
import time
import discord
import configparser
import sys
import os
import traceback
from discord.ext import commands


if not os.path.exists('config'):
    os.makedirs('config')

config_file = Path('config.ini')
if config_file.exists() is not True:
    sys.exit("I'm sorry, but i can't find your config file. Make sure to copy"
             + "the Config.ini.example as config.ini and insert your settings")

# parsing our config
config = configparser.ConfigParser()
config.read('config.ini')


def prefix_callable(bot, msg):
    user_id = bot.user.id
    prefixes =  [f'<@!{user_id}> ', f'<@{user_id}> ']
    prefixes.append('!') #use default ! prefix in DMs
    return prefixes

# Preparing the bot
bot = commands.AutoShardedBot(command_prefix=prefix_callable,
                   description='The silent coast guard of Discord servers.')


@bot.event
async def on_guild_join(guild: discord.Guild):
    bot.get_channel(544861813334867969)(f"A new guild came up: {guild.name} ({guild.id}).")


@bot.event
async def on_ready():
    if not bot.startup_done:
        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}' + f'\nVersion: {discord.__version__}\n')
        await BugLog.onReady(bot, config["Settings"]["botlog"])
        bot.startup_done = True
    await bot.change_presence(activity=discord.Activity(name='The Coastline.', type=discord.ActivityType.watching))


    @bot.event
async def on_message(message:discord.Message):
    if message.author.bot:
        return
    ctx:commands.Context = await bot.get_context(message)
    if ctx.command is not None:
        if isinstance(ctx.channel, discord.TextChannel) and not ctx.channel.permissions_for(ctx.channel.guild.me).send_messages:
            try:
                await ctx.author.send("Hey, you tried triggering a command in a channel I'm not allowed to send messages in. Please grant me permissions to reply and try again.")
            except Exception:
                pass #closed DMs
        else:
            await bot.invoke(ctx)


@commands.command(name='hello', aliases=['henlo', 'hey', 'hi'])
    async def hello(self, ctx: commands.Context, fren: discord.Member):
        """Checks the bot is running"""
        if fren is None:
            await ctx.send(f"Hey {ctx.author.mention} fren!")
        if fren = ctx.bot.user:
            await ctx.send("Hey there fren! I'm working for you.")
        if != ctx.author:
            await ctx.send(f"{fren.mention}: hey there fren! :) {ctx.author.mention}")


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



bot.run(config['Credentials']['Token'], bot=True)

time.sleep(5)
