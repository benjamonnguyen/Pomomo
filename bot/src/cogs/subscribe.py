from discord.ext import commands
from session import session_manager
from bot.configs import config, bot_enum


class Subscribe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dm(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            user = ctx.author
            subs = session.subscriptions.dm_subs
            if user in subs:
                subs.remove(user)
                await user.send(f'You\'ve been unsubscribed from DM alerts for {ctx.guild.name}.')
            else:
                subs.add(user)
                await user.send(f'Hey {user.display_name}! '
                                f'You are now subscribed to DM alerts for {ctx.guild.name}.\n'
                                f'Use command \'{config.CMD_PREFIX}dm\' in the server\'s text channel to unsubscribe.')

    @commands.command()
    async def auto_shush(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            if session.state == bot_enum.State.COUNTDOWN:
                await ctx.send('Auto-shush only works with pomodoro sessions.')
                return
            user = ctx.author
            subs = session.subscriptions.shush_subs
            if user in subs:
                if session.state == bot_enum.State.POMODORO:
                    await user.edit(deafen=False, mute=False)
                subs.remove(user)
                await user.send(f'You will no longer be automatically deafened and muted'
                                f' during pomodoro intervals in {ctx.guild.name}.')
            else:
                if session.state == bot_enum.State.POMODORO:
                    await user.edit(deafen=True, mute=True)
                subs.add(user)
                await user.send(f'Hey {user.display_name}! '
                                f'You will now be automatically deafened and muted '
                                f'during pomodoro intervals in {ctx.guild.name}.\n'
                                f'Use command \'{config.CMD_PREFIX}auto_shush\' in the server\'s '
                                f'text channel to turn off auto-shush.')


def setup(client):
    client.add_cog(Subscribe(client))
