
from discord.ext import commands
import discord
from sweater import config

bot = commands.Bot(intents=config.intents, command_prefix="e!")

import sweater.commands

bot.run(config.token)
