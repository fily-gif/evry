import contextlib
import discord
import asyncio
import re
import aiohttp
import datetime
import time
import os
import random
import sys
import platform
import json
import requests
import discord.utils
import dotenv
import io

from db import *
from discord.ext import *
from discord.ui import *
from datetime import datetime
from discord import *
from contextlib import *

db = UserDatabase(str(os.getenv("db")))

bot = discord.Bot()
evryclr = discord.Color.from_rgb(179, 134, 39)
intents = discord.Intents.default()
intents.members = True
start = time.time()
dotenv.load_dotenv() # loads the .env file

token = str(os.getenv("TOKEN"))
OWNERS = str(os.getenv("OWNERS" "clear_limit", "db")) 
creators = str(os.getenv("creators"))
clear_limit = int(os.getenv("clear_limit")) 

async def isfily(ctx):
    return ctx.author.id in OWNERS


def get_uptime():
    uptime = round((time.time() - start))

    if uptime <= 60:
        uptime = f'{str(uptime)} seconds'

    else:
        if uptime >= 60:
            uptime = f'{str(round(uptime/60, 2))} minutes'

        else:
            if uptime >= 3600:
                uptime = f'{str(round(uptime/60, 2))} hours'

            else:
                uptime = f'{str(uptime)} days'

    return uptime


def restart_bot():
    os.execv(sys.executable, ['python3'] + sys.argv)

@bot.slash_command(description="Get server information")
async def server(ctx):

    description = 'No description!'

    discord_timestamp = f"<t:{int(discord.utils.snowflake_time(ctx.guild.id).timestamp())}:F>"

    if ctx.guild.description is not None:

        description = ctx.guild.description

    embed = discord.Embed(title=f'{ctx.guild.name}', description=f'{description}', color=evryclr)

    embed.set_thumbnail(url=f'{ctx.guild.icon}')

    embed.add_field(name='Server ID', value=f'{ctx.guild.id}', inline=True)

    embed.add_field(name='Server Owner', value=f'{ctx.guild.owner}', inline=True)

    embed.add_field(name='Server Members', value=f'{ctx.guild.member_count}', inline=True)

    embed.add_field(name='Server Channels', value=f'{len(ctx.guild.channels)}', inline=True)

    embed.add_field(name='Server Roles', value=f'{len(ctx.guild.roles)}', inline=True)

    embed.add_field(name='Server Created At', value=discord_timestamp, inline=True)

    embed.set_footer(text=f'Made with ❤️ by {creators}')


    await ctx.respond(embed=embed)



@bot.command(description='Get help!')
async def help(ctx):
    # Get all the bot commands dynamically
    commands = bot.commands

    # Create the embed
    user = bot.user
    embed = discord.Embed(title=f'evry!', description=f'A bot that can do EVRYthing! [Invite me!](https://discord.com/api/oauth2/authorize?client_id=867167961181454356&permissions=1101860826326&scope=bot)', color=evryclr)

    # Loop through the commands and add them to the embed
    for command in commands:
        embed.add_field(name=f'/{command.name}', value=command.description, inline=True)

    # Add the thumbnail and footer
    embed.set_thumbnail(url=f'{user.avatar}')
    embed.set_footer(text=f'Made with ❤️ by {creators}')

    # Send the embed as response
    await ctx.respond(embed=embed)


@bot.slash_command(description='Returns discord <-> bot ping.')
async def ping(ctx):

    ping = round(bot.latency * 1000)

    await ctx.respond(f'Pong! ping is: **{ping}ms** <:AYAYA:962387316775739412>')
    print(f'{ping}ms')


@bot.slash_command(description='Delete messages in the chat. (requires manage messages permission)')
async def clear(ctx, amount: int):

    # check if the user has permission to use this command
    if ctx.author.guild_permissions.manage_messages:



        if int(amount) >= clear_limit:
            await ctx.respond('Too many messages to delete!')
            return

        await ctx.channel.purge(limit=amount+1)
        await ctx.respond(f'Deleted **{amount}** messages!')

    else:
        await ctx.respond('You do not have permission to use this command!')



@bot.slash_command(description='Add a reputation point to someone!')
async def rep(ctx, member: discord.Member):

    if not db.search_user(str(member.id)):
        db.add_user(str(member.id), member.name)

    db.add_reputation(str(member.id), 1)

    await ctx.respond(f'{ctx.author} added reputation to {member.name}!')


@bot.slash_command(description='Get someone\'s reputation!')
async def getrep(ctx, member: discord.Member):

    if not db.search_user(str(member.id)):
        db.add_user(str(member.id), member.name)

    rep_amount = db.get_reputation(str(member.id))

    await ctx.respond(f'{member.name}\'s rep is **{rep_amount}**.')


@bot.slash_command(description='Kick someone from the server. (requires manage users permission)')
async def kick(ctx, member: discord.Member, reason=None):


    if ctx.author.guild_permissions.kick_members:

        await member.kick(reason=reason)
        await ctx.respond(f'Kicked {member.mention} :hammer:')

        print(f'{ctx.message.replied_user} kicked {member.name}')

    else:
        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Ban someone from the server. (requires manage users permission)')
async def ban(ctx, member: discord.Member, reason=None):

    if ctx.author.guild_permissions.ban_members:

        await member.ban(reason=reason)
        await ctx.respond(f'Banned {member.mention} <:banhammer:962444283141562368>')

        print(f'{ctx.author} banned {member.name}')

    else:
        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Lift the banhammer from the user (requires manage users permission)')
async def unban(ctx, user_id):


    if ctx.author.guild_permissions.ban_members:

        try:
            user = await bot.fetch_user(user_id)

        except:
            await ctx.respond('Unknown user!')
            return

        await ctx.guild.unban(user)
        await ctx.respond(f'{user.mention} has been unbanned!')


@bot.slash_command(description='Set the slowmode for the channel. (requires manage channels permisison)')
async def slowmode(ctx, seconds=0):

    #check if the user has permission to use this command
    if ctx.author.guild_permissions.manage_channels:

        if seconds is None:

            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond('Slowmode has been reseted!')

            return

        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.respond(f'Slowmode set to {seconds} seconds :timer:')

    else:

        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Allows users with proper permissions to assign roles. (requires manage roles permisison)')
async def promote(ctx, role: discord.Role, member: discord.Member,):

    # check if the user has permission to use this command
    if ctx.author.guild_permissions.manage_roles:

        user = ctx.author

        if user.guild_permissions.manage_roles == True or ctx.author.id in OWNERS:

            await member.add_roles(role)
            await ctx.respond(f'{member.mention} has been promoted to {role}!')

        else:
            await ctx.respond('Not enough permissions! You need to have **manage roles** permission to execute this command!')

    else:
        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Remove a role from someone! (requires manage roles permission)')
async def demote(ctx, role: discord.Role, member: discord.Member):

    user = ctx.author

    if user.guild_permissions.manage_roles == True:

        await member.remove_roles(role)
        await ctx.respond(f'{member.mention} has been demoted from {role}!')

    else:
        await ctx.respond('Not enough permissions! You need to have **manage roles** permissions to execute this command!')


@bot.slash_command(description='Random numbers!')
async def roll(ctx, a: int, b: int):

    user = ctx.author

    roll = random.randint(a, b)
    await ctx.respond(f'You got {roll}!')


@bot.slash_command(description='Locks down the channel! (requires manage channels permission)')
async def lock(ctx, lock: bool):

    # check if the user has permission to use this command

    if ctx.author.guild_permissions.manage_channels == True:

        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)

        if lock is True:

            overwrite.send_messages = False

            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.respond('Channel locked down.')

        else:

            overwrite.send_messages = True

            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.respond('Channel unlocked.')

    else:

        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(descriptions='Get user\'s profile picture.')
async def avatar(ctx, member: discord.Member):

        username = f'{member.name}#{member.discriminator}'

        embed = discord.Embed(title=username, description=f'{member.name}\'s [avatar]({member.avatar})', color=evryclr)

        embed.set_image(url=member.avatar)
        embed.set_footer(text=f'Made with ❤️ by {creators}')

        await ctx.respond(embed=embed)


@bot.slash_command(description='get the information about the bot!')
async def about(ctx):
    embed = discord.Embed(title='Info', description=None, color=evryclr)
    embed.add_field(name='Python version', value=platform.python_version(), inline=True)
    embed.add_field(name='Pycord version', value=discord.__version__, inline=True)
    embed.add_field(name='Bot uptime', value=f'{get_uptime()}', inline=True)
    embed.add_field(name='Invite me!', value='[click!](https://discord.com/oauth2/authorize?client_id=867167961181454356&permissions=8&scope=bot)')
    embed.add_field(name='Made with ❤️', value=f'by {creators}', inline=True)

    await ctx.respond(embed=embed)


@bot.slash_command(description='Get a picture of a cute cat!')
async def cat(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/cat') as resp:
            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(title='random cat image! (=ↀωↀ=)', description='cat fact: ' + data['fact'], color=evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {creators}')
                await ctx.respond(embed=embed)

            else:
                await ctx.respond('Error getting cat image ¯\_(ツ)_/¯')


@bot.slash_command(description='Get a picutre of a cute dog!')
async def dog(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/dog') as resp:

            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(title='random dog image! ૮・ﻌ・ა', description='dog fact: ' + data['fact'], color=evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {creators}')
                await ctx.respond(embed=embed)

            else:

                await ctx.respond('Error getting dog image ¯\_(ツ)_/¯')


@bot.slash_command(description='Get a picture of a cute fox!')
async def fox(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/fox') as resp:

            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(
                    title='random fox image! 🦊', description='fox fact: ' + data['fact'], color=evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {creators}')
                await ctx.respond(embed=embed)

            else:

                await ctx.respond('Error getting fox image ¯\_(ツ)_/¯')


@bot.slash_command(description='Say something using the bot.')
async def say(ctx, message):

    embed = discord.Embed(
        title=f'A message from {ctx.author}', description=message, color=evryclr)
    embed.set_footer(text=f'{ctx.author}', icon_url=f'{ctx.author.avatar}')

    await ctx.respond(embed=embed)


@bot.slash_command(description='Change someone\'s nickname on the server. (requires manage nicknames permission)')
async def nickname(ctx, member: discord.Member, nick=None):

    #check if the user has permission to use this command

    if ctx.author.guild_permissions.manage_nicknames == True:

        if nick is None:

            await member.edit(nick=member.name)
            await ctx.respond(f'{member.name} has been reseted')
            return

        await member.edit(nick=nick)
        await ctx.respond(f'{member.name} has been changed to {nick}')

    else:

        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Set a reminder to do something.')
async def remind(ctx, seconds: int, message):

    await ctx.respond(f'I have set your reminder to {message} in {seconds}s')
    await asyncio.sleep(seconds)

    await ctx.send(f'{ctx.author.mention}, you have set a reminder to {message}')


@bot.slash_command(description='Random choice!')
async def choice(ctx, first: str, second: str):

    await ctx.respond(f'I choose... {random.choice([first, second])}')


@bot.slash_command(description='Gives you the weather!')
async def weather(ctx, city: str):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status == 200:

                data = await resp.json()

                sunset = datetime.fromtimestamp(
                    data['sys']['sunrise']).strftime('%H:%M')
                sunrise = datetime.fromtimestamp(
                    data['sys']['sunset']).strftime('%H:%M')

                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']

                city = data['name']

                description = f'{weather_description}, {temperature}°C.\n\nSunrise: {sunrise}, sunset: {sunset}'

                embed = discord.Embed(
                    title=f'Weather in {city}',
                    description=description
                )

                embed.set_footer(text=f'Made with ❤️ by {creators}')

                await ctx.respond(embed=embed, color=evryclr)

            else:
                await ctx.respond('An unknown error occured!')


@bot.slash_command(description='Random joke!')
async def joke(ctx):
    resp = requests.get('https://some-random-api.ml/joke')

    if resp.status_code == 200:

        joke = resp.json()['joke']

        await ctx.respond(joke)
        return

    else:
        await ctx.respond(f'Could not get the joke! {resp.status_code}')

@bot.slash_command(name='hex', description='Displays hex color.')
async def hex(ctx, color):

    pattern = re.compile(r'^[0-9a-f]+$', re.I)

    if pattern.search(color) and len(color) == 6:

        response = requests.get(url=f'https://some-random-api.ml/canvas/rgb?hex={color}')
        jsonData = json.loads(response.text)

        red = jsonData['r']
        green = jsonData['g']
        blue = jsonData['b']

        color = discord.Color.from_rgb(red, green, blue)

        embed = discord.Embed(title=f'Color 0x{color}', color=color)
        embed.set_image(url=f'https://some-random-api.ml/canvas/colorviewer?hex={color}')

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond('**Color argument is not hex number.**')

@bot.slash_command(description='calc')
async def calc(ctx, expression):

    allowed_chars = re.compile(r'^[0-9+\-*\/.() ]*$')

    if not allowed_chars.match(expression):
        result = "Invalid input"
    try:
        result = eval(expression)
        result = round(result, 2)
    except:
        result = "Invalid input"

    embed = discord.Embed(title=f'{expression} = {result}', color=evryclr)
    await ctx.respond(embed=embed)


@bot.slash_command(name="lyrics", description='Shows lyrics of song. (might not have some songs)')
async def lyrics(ctx, song_name):

    try:

        response = requests.get(f'https://some-random-api.ml/lyrics?title={song_name}')
        json_data = json.loads(response.text)

        error = json_data.get('error')

        if error:

            ctx.send(f'An error occured! {error}')
            return

        song_author = json_data['author']
        title = json_data['title']
        lyrics = json_data['lyrics']
        photo = list(json_data.get('thumbnail').items())[0][1]

        embed=discord.Embed(title=f'**{title}** by **{song_author}**', description=lyrics, url=photo, color=0xdb9e04)
        embed.set_thumbnail(url=photo)

        await ctx.respond(embed=embed)

    except Exception as e:
        ctx.send("Unknown error: {e}")

@bot.slash_command(description='Get a random color')
async def color(ctx):

    color = ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
    color = int(color, 16)
    color = discord.Colour(color)

    embed = discord.Embed(title='Random Color!', color=color)
    embed.set_image(
        url=f'https://placehold.it/1280x720/{color.value:06X}/fffrefff.png&text=')
    embed.description = f'Hex: #{color.value:06X}'
    embed.set_footer(text=f'Made with ❤️ by {creators}')
    await ctx.respond(embed=embed)

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def restart(ctx):

    if ctx.author.id in OWNERS:

        await ctx.respond('restarting!')
        restart_bot()

    else:
        await ctx.respond('Not enough permissions!')


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def cmd(ctx, *, code):
    if ctx.author.id in OWNERS:

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(code)

            exec(code)

        except Exception as e:
            await ctx.respond(f'```py\n{e}```')

        else:
            await ctx.respond(f'```py\n{stdout.getvalue()}```')


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def stop(ctx):

    if ctx.author.id in OWNERS:

        await ctx.respond('stopping!')
        exit()

    else:
        await ctx.respond('Not enough permissions!')


@bot.slash_command(name='effect', description='Applies effects on user\'s avatar.')
async def effect(ctx, filter: Option(choices=["blurple", "blur", "circle", "jpg"]), user: discord.Member):
    authorUrl = user.avatar

    if filter == 'blurple':

        embed = discord.Embed(title='Blurpify!', color=evryclr)
        embed.set_image(url=f'https://some-random-api.ml/canvas/blurple?avatar={str(authorUrl)}')
        await ctx.respond(embed=embed)

    elif filter =='blur':

        embed = discord.Embed(title='blur', color=evryclr)
        embed.set_image(url=f'https://some-random-api.ml/canvas/misc/blur?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)

    elif filter == 'circle':

        embed = discord.Embed(title='circleify!', color=evryclr)

        embed.set_image(url=f'https://some-random-api.ml/canvas/misc/circle?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)

    elif filter == 'jpg':
        embed = discord.Embed(title='JPG = Just Pretty Good', color=evryclr)
        embed.set_image(url=f'https://some-random-api.ml/canvas/misc/jpg?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)

@bot.event
async def on_ready():

    evry = bot.user
    ping = round(bot.latency * 1000)

    os.system('clear')
    print(f'{evry} {evry.id}')
    print(f'{ping}ms')
    print('--------------------------------')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music!"))

bot.run(token)
