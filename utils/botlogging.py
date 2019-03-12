import sys
import datetime
import logging
import traceback
import time
import configparser
import discord
from discord.ext import commands
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger('GhostGuard')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='GhostGuard.log', encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

BOT_LOGGING_CHANNEL:discord.TextChannel

startupErrors = []


def info(message):
    logger.info(message)


def warn(message):
    logger.warning(message)


def error(message):
    logger.error(message)

def exception(message, error):
    logger.error(message)
    logger.error(traceback.format_tb(error.__traceback__))


#If the bot errors before startup is complete
def startupError(message, error):
    logger.exception(message)
    startupErrors.append({
        "message": message,
        "exception": error,
        "stacktrace": traceback.format_exc().splitlines()
    })

async def onReady(bot: commands.Bot):
    global BOT_LOG_CHANNEL, BOT
    BOT = bot
    BOT_LOG_CHANNEL = bot.get_channel(config['Settings']['botlogger'])
    if BOT_LOG_CHANNEL is None:
        logger.error("Logging channel is misconfigured, aborting startup!")
        await bot.logout()
    info = await bot.application_info()

    if len(STARTUP_ERRORS) > 0:
        await bot_log(
            f":rotating_light: Caught {len(STARTUP_ERRORS)} {'exceptions' if len(STARTUP_ERRORS) > 1 else 'exception'} during startup.")
        for e in STARTUP_ERRORS:
            await e
        STARTUP_ERRORS = []
async def bot_log(message=None, embed=None):
    if BOT_LOG_CHANNEL is not None:
        return await BOT_LOG_CHANNEL.send(content=message, embed=embed)
    else:
        STARTUP_ERRORS.append(bot_log(message, embed))
