from sweater import bot
import discord
import sweater.config as config
import os
import sweater.utils as utils

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def restart(ctx):

    if ctx.author.id in config.owners:

        await ctx.respond('restarting!')
        utils.restart_bot()

    else:
        await ctx.respond('Not enough permissions!')


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def pull(ctx, hash=None):

        if ctx.author.id in config.owners:

            if hash is None:
                hash = utils.last_githash()

            else:
                hash = hash

            await ctx.respond(f'pulling {hash}')
            os.system('git init && git pull') # if this fails get git
            ctx.send('pulled! restarting the bot...')
            utils.restart_bot()

        else:
            await ctx.respond('Not enough permission!')


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def stop(ctx):

    if ctx.author.id in config.owners:

        await ctx.respond('stopping!')
        exit(1)

    else:
        await ctx.respond('Not enough permissions!')

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def tell(ctx, message, channel: discord.TextChannel):

    if ctx.author.id in config.owners:

        await ctx.send(message)
        await ctx.respond('Message sent!', ephemeral=True)

    else:
        await ctx.respond('Not enough permissions!')

