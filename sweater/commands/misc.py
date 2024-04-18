import random
from sweater import bot
import sweater.config as config
import asyncio
import discord
import re
import aiohttp
import io

@bot.slash_command(description='Random numbers!')
async def roll(ctx, a: int, b: int):

    roll = random.randint(a, b)
    await ctx.respond(f'You got {roll}!')

@bot.slash_command(description='Set a reminder to do something.')
async def remind(ctx, seconds: int, message):

    await ctx.respond(f'I have set your reminder to {message} in {seconds}s')
    await asyncio.sleep(seconds)

    await ctx.send(f'{ctx.author.mention}, you have set a reminder to {message}')

@bot.slash_command(description='calculate something')
async def calc(ctx, expression):

    #allows only numbers, +, -, *, /, ., (, ), and spaces, but not "**"
    allowed_chars = re.compile(r'^[0-9\+\-\*\/\. ]$')

    try:
        result = eval(expression)
    except Exception as e:
        embed = discord.Embed(title=f'{expression} is not a valid input!', color=config.evryclr)
        print(e)

    if not allowed_chars.search(expression):
        result = round(result, 2)

    embed = discord.Embed(title=f'{expression} = {result}', color=config.evryclr)
    await ctx.respond(embed=embed)


@bot.slash_command(description='Send feedback!')
async def feedback(ctx, message):

    user = await bot.fetch_user(831530536781873163)

    await user.send(f'\"{message}\" by {ctx.author} ({ctx.author.id})')
    await ctx.respond('feedback sent!')

@bot.slash_command(description='Get user\'s profile picture.')
async def avatar(ctx, member: discord.Member):
    username = f'{member.name}'  # assume that the target has pomelo
    avatar_url = str(member.avatar)  # ??

    if member.discriminator != '0':
        username = f'{member.name}#{member.discriminator}'

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as resp:
            if resp.status != 200:
                return await ctx.respond("An error occured!")
            data = io.BytesIO(await resp.read())

    embed = discord.Embed(color=config.evryclr, title=f'{username}\'s avatar!')
    embed.set_image(url='attachment://avatar.url')
    embed.set_footer(text=f'made with ❤️ by {config.creators}')

    await ctx.respond(file=discord.File(data, 'upload.png'), embed=embed)
