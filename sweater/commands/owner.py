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
async def pull(ctx):

        if ctx.author.id in config.owners:
            await ctx.respond(f'pulling {hash}')
            try:
                os.system('git init && git pull') # if this fails get git
                ctx.send('pulled! restarting the bot...')
            except Exception as e:
                ctx.send(f'Error: {e}\n\nIs git installed?')
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
async def tell(ctx, message, channel: discord.TextChannel = None, user: discord.User = None):

    if ctx.author.id in config.owners:

        if user is not None:
            user = bot.get_user(user.id)
            await user.send(message)
            await ctx.respond('Message sent!', ephemeral=True)
            pass
        else:
            pass

        if channel is not None:
            channel = bot.get_channel(channel.id)
            await channel.send(message)
            await ctx.respond('Message sent!', ephemeral=True)
        else:
            pass

    else:
        await ctx.respond('Not enough permissions!')

