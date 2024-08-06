import discord
import aiohttp
import requests

from sweater import bot 
import sweater.config as config 

@bot.slash_command(description='Gives you the weather!')
async def weather(ctx, city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                sunrise = data['sys']['sunrise']
                sunset = data['sys']['sunset']
                
                # Format timestamps directly
                sunrise_formatted = f"<t:{sunrise}:t>"
                sunset_formatted = f"<t:{sunset}:t>"
                
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                city = data['name']
                description = f'Weather description: {weather_description}, {temperature}°C.\n\nSunrise: {sunrise_formatted}, Sunset: {sunset_formatted}'
                embed = discord.Embed(title=f'Weather in {city}', description=description, color=config.evryclr)
                embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                await ctx.respond(embed=embed)
            else:
                await ctx.respond('An unknown error occurred!')


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


@bot.slash_command(description='Get information about a minecraft server!')
async def mcserver(ctx, server):
    url = f'https://api.mcsrvstat.us/2/{server}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data['online']:
                    description = f"Server IP: {data['ip']}\nPlayers: {data['players']['online']}/{data['players']['max']}\nVersion: {data['version']}"
                    embed = discord.Embed(title=f'{server} Server', description=description, color=config.evryclr)
                    embed.set_thumbnail(url=f"https://api.mcsrvstat.us/icon/{server}")
                    embed.set_footer(text=f'Made with ❤️ by {config.creators}')
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond('Server is offline!')
            else:
                await ctx.respond('An unknown error occurred!')


@bot.slash_command(description='Random joke!')
async def joke(ctx):
    resp = requests.get('https://some-random-api.com/joke')

    if resp.status_code == 200:

        joke = resp.json()['joke']

        await ctx.respond(joke)
        return

    else:
        await ctx.respond(f'Could not get the joke! The API returned {resp.status_code}')
