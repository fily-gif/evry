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

class arrows(discord.ui.View):

    def commands_set(self, commands):
            self.commands = commands

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="<:goright:1205006549727322123>")
    async def button_callback(self, button, interaction):

        embed = discord.Embed(title='evry!', description='A bot that can do EVRYthing! [Invite me!](https://discord.com/api/oauth2/authorize?client_id=867167961181454356&permissions=1101860826326&scope=bot)', color=config.evryclr)

        [embed.add_field(name=f'/{command.name}', value=command.description, inline=True) for command in self.commands[1]]

        await interaction.edit_original_message(embed=embed) 

@bot.slash_command(description='Get help!')
async def help(ctx):
# https://guide.pycord.dev/extensions/pages/paginator-basics
    commands = bot.commands
    user = bot.user
    embed = discord.Embed(title='evry!', description='A bot that can do EVRYthing! [Invite me!](https://discord.com/api/oauth2/authorize?client_id=867167961181454356&permissions=1101860826326&scope=bot)', color=config.evryclr)

    chunk_size = 25
    commands_chunks = [commands[i:i + chunk_size] for i in range(0, len(commands), chunk_size)]

    [embed.add_field(name=f'/{command.name}', value=command.description, inline=True) for command in commands_chunks[0]]

    # Add the thumbnail and footer
    embed.set_thumbnail(url=f'{user.avatar}')
    embed.set_footer(text=f'Made with ❤️ by {config.creators}')

    arrows_obj = arrows()
    arrows_obj.commands_set(commands_chunks)

    # Send the embed as response
    await ctx.respond(embed=embed, view=arrows_obj)

@bot.slash_command(description='Returns discord <-> bot ping.')
async def ping(ctx):

    ping = round(bot.latency * 1000)

    await ctx.respond(f'Pong! ping is: **{ping}ms** <:AYAYA:962387316775739412>')
    print(f'{ping}ms')


@bot.slash_command(description='get the information about the bot!')
async def about(ctx):
    embed = discord.Embed(title='Info', description=None, color=config.evryclr)
    embed.add_field(name='Python version', value=platform.python_version(), inline=True)
    embed.add_field(name='Pycord version', value=discord.__version__, inline=True)
    embed.add_field(name='Bot uptime', value=utils.get_uptime(), inline=True)
    embed.add_field(name='Invite me!', value=f'[click!](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=1514446122198&scope=bot)', inline=True)
    embed.add_field(name='CPU usage', value=f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(name='RAM usage', value=f'{psutil.virtual_memory().percent}%', inline=True)
    embed.add_field(name='Host', value=f'{platform.system()}, {platform.release()}', inline=True)
    embed.add_field(name='Git hash', value=f'{utils.last_githash()}')

    embed.add_field(name='Made with ❤️', value=f'by {config.creators}')

    await ctx.respond(embed=embed)
