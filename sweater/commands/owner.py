from sweater import bot
import discord
import sweater.config as config
import io
import contextlib
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
async def cmd(ctx, *, code):
    if ctx.author.id in config.owners:
        stdout = io.StringIO()

        try:

            with contextlib.redirect_stdout(stdout):

                exec(f'async def _exec(ctx):\n    {code}')
                await locals()['_exec'](ctx=ctx)

        except Exception as e:
            await ctx.respond(f'```py\n{e}```')

        else:
            await ctx.respond(f'```py\n{stdout.getvalue()}```')

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def stop(ctx):

    if ctx.author.id in config.owners:

        await ctx.respond('stopping!')
        exit()

    else:
        await ctx.respond('Not enough permissions!')


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def pull(ctx, hash=None):
    
        if ctx.author.id in config.owners:
    
            if hash is None:
                hash = utils.last_githash()

            await ctx.respond(f'pulling {hash}')
            os.system(f'git pull https://github.com/fily-gif/evry.git') # if this fails get git
            ctx.send('pulled! restarting the bot...')
            utils.restart_bot()
        
        elif hash is not None:
            ctx.respond(f'pulling {hash} (**BOILERPLATE**)')

        else:
            await ctx.respond('Not enough permissions!')



@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def tell(ctx, message, channel: discord.TextChannel):

    if ctx.author.id in config.owners:

        await ctx.send(message)
        await ctx.respond('Message sent!', ephemeral=True)

    else:
        await ctx.respond('Not enough permissions!')

