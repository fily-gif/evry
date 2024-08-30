import discord
import platform
import psutil
from sweater import bot
import sweater.utils as utils
import sweater.config as config

@bot.slash_command(description="Get server information")
async def server(ctx):

    guild = ctx.guild
    description = 'No description!'
    discord_timestamp = f"<t:{int(discord.utils.snowflake_time(guild.id).timestamp())}:F>"

    if guild.description is not None:
        description = guild.description

    embed = discord.Embed(title=f'{guild.name}', description=f'{description}', color=config.evryclr)

    embed.set_thumbnail(url=f'{guild.icon}')

    embed.add_field(name='Server ID', value=f'{guild.id}', inline=True)
    embed.add_field(name='Server Owner', value=f'{guild.owner.name}', inline=True)
    embed.add_field(name='Server Members', value=f'{guild.member_count}', inline=True)
    embed.add_field(name='Server Channels', value=f'{len(guild.channels)}', inline=True)
    embed.add_field(name='Server Roles', value=f'{len(guild.roles)}', inline=True)
    embed.add_field(name='Server Created At', value=discord_timestamp, inline=True)

    embed.set_footer(text=f'Made with ❤️ by {config.creators}')


    await ctx.respond(embed=embed)


@bot.slash_command(description='Returns discord <-> bot ping.')
async def ping(ctx):

    ping = round(bot.latency * 1000)

    await ctx.respond(f'Pong! Ping is: **{ping}ms** <:AYAYA:962387316775739412>')
    print(f'{ping}ms')


@bot.slash_command(description='Get the information about the bot!')
async def about(ctx):
    embed = discord.Embed(title='Info', description=None, color=config.evryclr)
    embed.add_field(name='Python version', value=platform.python_version(), inline=True)
    embed.add_field(name='Pycord version', value=discord.__version__, inline=True)
    embed.add_field(name='Bot uptime', value=utils.get_uptime(), inline=True)
    embed.add_field(name='Invite me!', value=f'[click!](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=1514446122198&scope=bot)', inline=True)
    embed.add_field(name='CPU usage', value=f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(name='RAM usage', value=f'{psutil.virtual_memory().percent}%', inline=True)
    embed.add_field(name='Host', value=f'{platform.system()}, {platform.release()}', inline=True)
    embed.add_field(name='Git hash', value=f'{utils.last_githash()}')

    embed.add_field(name='Made with ❤️', value=f'by {config.creators}')

    await ctx.respond(embed=embed)
