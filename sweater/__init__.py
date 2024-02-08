
from discord.ext import commands
import discord
from sweater import config

bot = discord.Bot(intents=config.intents, command_prefix="-")

import sweater.commands

bot.run(config.token)
