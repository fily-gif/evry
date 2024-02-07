from sweater import bot
import discord
import sweater.config as config
import os
import ast
import sweater.utils as utils
import sweater.config

@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def restart(ctx):

    if ctx.author.id in config.owners:

        await ctx.respond('restarting!')
        utils.restart_bot()

    else:
        await ctx.respond('Not enough permissions!')

@bot.command()
async def tt(ctx, code):
    if ctx.author.id in config.owners:
        try:
            cmd = code.strip('` ')
            fn_name = "funny"
            cmd = "\n".join(f' {i}' for i in code.splitlines())
            body = f"async def {fn_name}(cmd):\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            utils.insert_returns(body)

            env = {
                "bot": ctx.bot,
                "discord": discord,
                "ctx": ctx,
                "__import__": __import__,
                "config": sweater.config,
                "utils": sweater.utils,
                "os": os
            }

            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = await str(eval(f"await {fn_name}()", env))

            if config.token not in result:
                await ctx.send(f'```py\n{str(result)}\n```')

            else:
                await ctx.send('guh, nice try')

        except Exception as e:
            await ctx.send(e)

    else:
        ctx.send("Not enough permissions!")

@bot.command()
async def cmd(ctx, *, code):
    if ctx.author.id in config.owners:
        try:

            cmd = code.strip('` ')
            fn_name = "funny"
            cmd = "\n".join(f"  {i}" for i in code.splitlines())
            body = f"async def {fn_name}(cmd):\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            utils.insert_returns(body)

            env = {
                "bot": ctx.bot,
                "discord": discord,
                "ctx": ctx,
                "__import__": __import__,
                "config": sweater.config,
                "utils": sweater.utils,
                "os": os
            }

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await str(eval(f"await {fn_name}()", env))

            if config.token not in result:
                await ctx.respond(f"```py\n{str(result)}\n```")

            else:
                await ctx.respond("guh, nice try")

        except Exception as e:
            await ctx.respond(f"error! {e}")

    else:
        await ctx.respond("Not enough permissions!")


@bot.slash_command(description='!!OWNER ONLY!!, this will not work if you are not fily')
async def pull(ctx, hash=None):

        if ctx.author.id in config.owners:

            if hash is None:
                hash = utils.last_githash()

            await ctx.respond(f'pulling {hash}')
            os.system('git pull https://github.com/fily-gif/evry.git') # if this fails get git
            await ctx.send('pulled! restarting the bot...')
            utils.restart_bot()

        elif hash is not None:
            ctx.respond(f'pulling {hash} (**BOILERPLATE**)')

        else:
            await ctx.respond('Not enough permissions!')

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

