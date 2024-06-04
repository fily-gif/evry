import discord
from discord import Option
import aiohttp
import datetime
import requests
import random
import json
import re
import io

from sweater import bot 
import sweater.config as config 
import sweater.utils as utils

@bot.slash_command(description='Gives you the weather!')
async def weather(ctx, city: str):

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status == 200:

                data = await resp.json()

                sunset = f"<t:{data['sys']['sunset']}:t>" #datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                sunrise = f"<t:{data['sys']['sunrise']}:t>" #datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')

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
async def hex(ctx, color: str):
    pattern = re.compile(r'^[0-9a-fA-F]{6}$')

    if color.startswith("#"):
        color = color[1:]

    if pattern.match(color):

        img = utils.hex_to_img(color)

        # Convert the image to bytes
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)

            # Create a discord file from the image bytes
            discord_file = discord.File(fp=image_binary, filename=f'{color}.png')

        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        discord_color = discord.Color.from_rgb(r, g, b)

        embed = discord.Embed(title=f'Color #{color}', color=discord_color)
        embed.set_image(url=f'attachment://{color}.png')
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        await ctx.respond(embed=embed, file=discord_file)

    else:
        await ctx.respond('**Color argument is not a valid hex number.**')


@bot.slash_command(description='Get a random color')
async def color(ctx):
    color = random.randint(0, 0xFFFFFF)
    color = discord.Colour(color)

    img = utils.hex_to_img(str(color))

    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)

        discord_file = discord.File(fp=image_binary, filename=f'{color}.png')

    embed = discord.Embed(title='Random color!', color=color)
    embed.set_image(url=f'attachment://{color}.png')
    embed.description = f'Hex: #{color.value:X}'
    embed.set_footer(text=f'Made with ❤️ by {config.creators}')
    await ctx.respond(embed=embed, file=discord_file)