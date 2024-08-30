import discord
from sweater import bot
import sweater.config as config

@bot.slash_command(description='Kick someone from the server. (requires manage users permission)')
async def kick(ctx, member: discord.Member, reason=None):

    if ctx.author.guild_permissions.kick_members:

        await member.kick(reason=reason)
        await ctx.respond(f'Kicked {member.mention} :hammer:')

        print(f'{ctx.message.replied_user} kicked {member.name}')

    else:
        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Ban someone from the server. (requires manage users permission)')
async def ban(ctx, member: discord.Member, reason=None):

    if ctx.author.guild_permissions.ban_members:

        await member.ban(reason=reason)
        await ctx.respond(f'Banned {member.mention} <:banhammer:962444283141562368>')

        print(f'{ctx.author} banned {member.name}')

    else:
        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Lift the banhammer from the user (requires manage users permission)')
async def unban(ctx, user_id):


    if ctx.author.guild_permissions.ban_members:

        try:
            user = await bot.fetch_user(user_id)

        except:
            await ctx.respond('Unknown user!')
            return

        await ctx.guild.unban(user)
        await ctx.respond(f'{user.mention} has been unbanned!')


@bot.slash_command(description='Set the slowmode for the channel. (requires manage channels permisison)')
async def slowmode(ctx, seconds=0):

    #check if the user has permission to use this command
    if ctx.author.guild_permissions.manage_channels:

        print(f"{seconds}s") #?? was this for debug??
        if seconds is None or 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.respond('Slowmode has been reset!')

            return

        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.respond(f'Slowmode set to {seconds} seconds :timer:')

    else:

        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Allows users to assign roles. (requires manage roles permisison)')
async def promote(ctx, role: discord.Role, member: discord.Member,):
        user = ctx.author

        if user.guild_permissions.manage_roles:

            await member.add_roles(role)
            await ctx.respond(f'{member.mention} has been promoted to {role}!')

        else:
            await ctx.respond('Not enough permissions! You need to have **manage roles** permission to execute this command!')


@bot.slash_command(description='Remove a role from someone! (requires manage roles permission)')
async def demote(ctx, role: discord.Role, member: discord.Member):

    user = ctx.author

    if user.guild_permissions.manage_roles:

        await member.remove_roles(role)
        await ctx.respond(f'{member.mention} has been demoted from {role}!')

    else:
        await ctx.respond('Not enough permissions! You need to have **manage roles** permissions to execute this command!')


@bot.slash_command(description='Change someone\'s nickname on the server. (requires manage nicknames permission)')
async def nickname(ctx, member: discord.Member, nick=None):

    #check if the user has permission to use this command

    if ctx.author.guild_permissions.manage_nicknames:

        try:

            if nick is None:

                await member.edit(nick=member.name)
                await ctx.respond(f'{member.name} has been reset')
                return

            await member.edit(nick=nick)
            await ctx.respond(f'{member.name} has been changed to {nick}')

        except discord.ext.commands.MissingPermissions or discord.ext.commands.BotMissingPermissions as e:

            await ctx.respond(f'Eiher you or evry does not have permission to do this! [{e}]')
            print(e)

    else:

        await ctx.respond('You do not have permission to use this command!')


@bot.slash_command(description='Delete messages in the chat. (requires manage messages permission)')
async def clear(ctx, amount: int = 1):

    # check if the user has permission to use this command
    if ctx.author.guild_permissions.manage_messages:
        if int(amount) >= config.clear_limit:
            await ctx.respond(f'Too many messages to delete! [max: {config.clear_limit}]')
            return

        await ctx.channel.purge(limit=amount)
        await ctx.respond(f'Deleted **{amount}** messages!')

    else:
        await ctx.respond('You do not have permission to use this command!')