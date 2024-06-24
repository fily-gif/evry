import re
import random
from sweater import bot
import sweater.config as config
import sweater.utils as utils
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

@bot.slash_command(name='hex', description='Displays hex color.')
async def hex(ctx, color: str):
    pattern = re.compile(r'^[0-9a-fA-F]{6}$')

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
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)

        await ctx.respond(embed=embed, file=discord_file)

    else:
        await ctx.respond('**Color argument is not a valid hex number.**')


@bot.slash_command(description='Get a random color')
async def color(ctx):
    color = "{:06x}".format(random.randint(0, 0xFFFFFF))
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
    embed.description = f'Hex: #{color}'
    embed.set_footer(text=f'Made with :heart: by {config.creators}')
    await ctx.respond(embed=embed, file=discord_file)
