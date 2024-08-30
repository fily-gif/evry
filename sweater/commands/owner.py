from sweater import bot
import discord
import sweater.config as config
import os
import sweater.utils as utils
import asyncio
import ast

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
            await ctx.respond(f'pulling {utils.last_githash()}...')
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

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def eeval(ctx, *, code: str):

    if ctx.author.id in config.owners:

        env = {
            'bot': bot,
            'discord': discord,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'config': config,
            'utils': utils,
            'os': os
        }

        def async_exec(code, env):
            exec(f'async def __ex(): ' + ''.join(f'\n {l}' for l in code.split('\n')), env)
            return env['__ex']()
        try:
            try:
                parsed = ast.literal_eval(code)
            except:
                try:
                    parsed = eval(code, globals(), env)
                except SyntaxError:
                    parsed = async_exec(code, env)

            if asyncio.iscoroutine(parsed):
                parsed = await parsed
            if config.token in str(parsed):
                await ctx.respond('Token detected! Nice try.')
                return
            await ctx.respond(f"```py\n{parsed}\n```")
        except Exception as e:
            await ctx.respond(f"```py\n{e}\n```")

    else:
        await ctx.respond('Not enough permissions!')

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def blocklist(ctx, user: discord.Member):
	if user.id in config.blocklist:
		await ctx.respond('User is already in the blocklist!')
	else:
		blocklist.append(user.id)
		await ctx.respond(f'{user.mention} has been added to the blocklist!')