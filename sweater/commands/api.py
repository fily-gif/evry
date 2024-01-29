import discord
from discord import Option
import aiohttp
import datetime
import requests
import random
import json
import re

from sweater import bot 
import sweater.config as config 

@bot.slash_command(description='Gives you the weather!')
async def weather(ctx, city: str):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status == 200:

                data = await resp.json()

                sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')

                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']

                city = data['name']

                description = f'Weather description: {weather_description}, {temperature}°C.\n\nSunrise: {sunrise}, sunset: {sunset}'

                embed = discord.Embed(title=f'Weather in {city}', description=description, color=config.evryclr)

                embed.set_footer(text=f'Made with ❤️ by {config.creators}')

                await ctx.respond(embed=embed)

            else:
                await ctx.respond('An unknown error occured!')
                print('test')
                


@bot.slash_command(description='Get a picture of a cute cat!')
async def cat(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.com/animal/cat') as resp:
            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(title='random cat image! (=ↀωↀ=)', description='cat fact: ' + data['fact'], color=config.evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                await ctx.respond(embed=embed)

            else:
                await ctx.respond('Error getting cat image ¯\_(ツ)_/¯')


@bot.slash_command(description='Get a picutre of a cute dog!')
async def dog(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.com/animal/dog') as resp:

            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(title='random dog image! ૮・ﻌ・ა', description='dog fact: ' + data['fact'], color=config.evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                await ctx.respond(embed=embed)

            else:

                await ctx.respond('Error getting dog image ¯\_(ツ)_/¯')


@bot.slash_command(description='Get a picture of a cute fox!')
async def fox(ctx):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.com/animal/fox') as resp:

            if resp.status == 200:

                data = await resp.json()
                embed = discord.Embed(
                    title='random fox image! 🦊', description='fox fact: ' + data['fact'], color=config.evryclr)
                embed.set_image(url=data['image'])
                embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                await ctx.respond(embed=embed)

            else:

                await ctx.respond('Error getting fox image ¯\_(ツ)_/¯')


@bot.slash_command(description='Random joke!')
async def joke(ctx):
    resp = requests.get('https://some-random-api.com/joke')

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

        response = requests.get(url=f'https://some-random-api.com/canvas/rgb?hex={color}')
        jsonData = json.loads(response.text)

        red = jsonData['r']
        green = jsonData['g']
        blue = jsonData['b']

        color = discord.Color.from_rgb(red, green, blue)

        embed = discord.Embed(title=f'Color 0x{color}', color=color)
        embed.set_image(url=f'https://some-random-api.com/canvas/colorviewer?hex={color}')

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond('**Color argument is not hex number.**')


@bot.slash_command(description='Get a random color')
async def color(ctx):

    color = ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
    color = int(color, 16)
    color = discord.Colour(color)

    embed = discord.Embed(title='Random Color!', color=color)
    embed.set_image(
        url=f'https://placehold.it/1280x720/{color.value:06X}/fffrefff.png&text=')
    embed.description = f'Hex: #{color.value:06X}'
    embed.set_footer(text=f'Made with ❤️ by {config.creators}')
    await ctx.respond(embed=embed)


@bot.slash_command(name='effect', description='Applies effects on user\'s avatar.')
async def effect(ctx, filter: Option(choices=["blurple", "blur", "circle", "jpg"]), user: discord.Member):
    authorUrl = user.avatar

    if filter == 'blurple':

        embed = discord.Embed(title='Blurpify!', color=config.evryclr)
        embed.set_image(url=f'https://some-random-api.com/canvas/blurple?avatar={str(authorUrl)}')
        await ctx.respond(embed=embed)

    elif filter =='blur':

        embed = discord.Embed(title='blur', color=config.evryclr)
        embed.set_image(url=f'https://some-random-api.com/canvas/misc/blur?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)

    elif filter == 'circle':

        embed = discord.Embed(title='circleify!', color=config.evryclr)

        embed.set_image(url=f'https://some-random-api.com/canvas/misc/circle?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)

    elif filter == 'jpg':
        embed = discord.Embed(title='JPG = Just Pretty Good', color=config.evryclr)
        embed.set_image(url=f'https://some-random-api.com/canvas/misc/jpg?avatar={str(authorUrl)[:-10]}')
        await ctx.respond(embed=embed)
