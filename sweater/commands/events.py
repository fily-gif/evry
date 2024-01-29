from sweater import bot
import os
import discord
import random


@bot.event
async def on_guild_join(guild):

    server = 959153143046881323

    channel = bot.get_channel(server)

    await channel.send(f'Joined {guild.name} ({guild.id}), owned by {guild.owner}')

    print(f'Joined {guild.name} ({guild.id}), owned by {guild.owner} ({guild.owner_id})')

@bot.event
async def on_ready():

    evry = bot.user
    ping = round(bot.latency * 1000)

    """if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')"""
    print(f'{evry} {evry.id}')
    print(f'{ping}ms')
    print(f'{"-"*18}')

    status = ['with /-commands!', 'with fily!', 'with evrything!']
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(status)))

