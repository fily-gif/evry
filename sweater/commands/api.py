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

                sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')

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


@bot.slash_command(description='Get the urban dictionary definition!')
async def urban(ctx, term):
    
        url = f'https://api.urbandictionary.com/v0/define?term={term}'
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
    
                if resp.status == 200:
    
                    data = await resp.json()
    
                    if len(data['list']) == 0:
                        await ctx.respond('No definition found!')
                        return
    
                    definition = data['list'][0]
                    actual = definition['definition'].replace('[', '').replace(']', '')
    
                    embed = discord.Embed(title=term, description=actual, color=config.evryclr)
                    embed.add_field(name='Example:', value=definition['example'])
                    embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                    await ctx.respond(embed=embed)
    
                else:
                    await ctx.respond('An unknown error occured!')


@bot.slash_command(description='Random joke!')
async def joke(ctx):
    resp = requests.get('https://some-random-api.com/joke')

    if resp.status_code == 200:

        joke = resp.json()['joke']

        await ctx.respond(joke)
        return

    else:
        await ctx.respond(f'Could not get the joke! The API returned {resp.status_code}')

@bot.slash_command(name='hex', description='Displays hex color.')
async def hex(ctx, color):

    pattern = re.compile(r'^[0-9a-f]+$', re.I)

    if pattern.search(color) and len(color) == 6:

        response = requests.get(url=f'https://placehold.it/480x480/{color.value}/fffrefff.png&text=')
        jsonData = json.loads(response.text)

        red = jsonData['r']
        green = jsonData['g']
        blue = jsonData['b']

        color = discord.Color.from_rgb(red, green, blue)

        embed = discord.Embed(title=f'Color 0x{color}', color=color)
        embed.set_image(url=f'https://placehold.it/480x480/{color.value}/fffrefff.png&text=')

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond('**Color argument is not hex number.**')


@bot.slash_command(description='Get a random color')
async def color(ctx):

    color = random.randint(0, 0xFFFFFF)
    color = discord.Colour(color)

    embed = discord.Embed(title='Random Color!', color=color)
    embed.set_image(
        url=f'https://placehold.it/480x480/{color.value}/fffrefff.png&text=')
    embed.description = f'Hex: #{color.value:X}'
    embed.set_footer(text=f'Made with ❤️ by {config.creators}')
    await ctx.respond(embed=embed)