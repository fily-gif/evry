
from discord.ext import commands
import discord
from sweater import config

bot = discord.Bot(intents=config.intents)

import sweater.commands

bot.run(config.token)
