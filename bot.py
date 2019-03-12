#!/usr/bin/env python3
import asyncio
import datetime
import time
import discord
import configparser
import sys
import os
import traceback
from discord.ext import commands
from pathlib import Path
from utils import botlogging

ctx = commands.Context

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
bot = commands.AutoShardedBot(command_prefix=prefix_callable, case_insensitive=True, owner_id=189878809997213706,
                   description='The silent coast guard of Discord servers.')


initial_extensions = ['basic']


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
        except:
            print(f"Failed to load extension {extension}.")


@bot.event
async def on_guild_join(guild: discord.Guild):
    await BOT_LOG_CHANNEL.send(f"A new guild came up: {guild.name} ({guild.id}).")
    await botlogging.info(f"A new guild came up: {guild.name} ({guild.id}).")


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}' + f'\nVersion: {discord.__version__}\n')
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


bot.run(config['Credentials']['Token'], bot=True)


time.sleep(5)
