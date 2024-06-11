import random
from sweater import bot
import sweater.config as config
import asyncio
import discord
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


@bot.slash_command(description='Send feedback!')
async def feedback(ctx, message):

    user = await bot.fetch_user(config.owners[0])

    await user.send(f'\"{message}\" by {ctx.author} ({ctx.author.id})')
    await ctx.respond('feedback sent!', ephemeral=True)

@bot.slash_command(description='Get user\'s profile picture.')
async def avatar(ctx, member: discord.Member):
    username = f'{member.name}'  # assume that the target has pomelo
    avatar_url = str(member.display_avatar)  # ??

    if member.discriminator != '0':
        username = f'{member.name}#{member.discriminator}'

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as resp:
            if resp.status != 200:
                return await ctx.respond("An error occured!")
            data = io.BytesIO(await resp.read())

    await ctx.respond(f'{username}\'s avatar!', file=discord.File(data, 'upload.png'))
