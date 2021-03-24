from discord.ext import commands
from utils import msg_builder
import user_messages as u_msg
import config
from Session import session_manager, Session


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=''):
        await ctx.send(msg_builder.help_msg(command))

    @commands.command()
    async def time(self, ctx):
        session = session_manager.active_sessions.get(ctx.guild.id)
        if not session:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        await ctx.send(f'{session.timer.time_remaining_to_str()} remaining on {session.state}!')

    @commands.command()
    async def settings(self, ctx):
        session = session_manager.active_sessions.get(ctx.guild.id)
        if not session:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        msg = 'Session settings:\n\n' + \
              msg_builder.settings_msg(session.settings)
        await ctx.send(msg)

    @commands.command()
    async def dm(self, ctx):
        session: Session = session_manager.active_sessions.get(ctx.guild.id)
        if not session:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        user = ctx.author
        subs = session.subscribers
        if user in subs:
            subs.remove(user)
            await user.send(f'You\'ve been unsubscribed from DM alerts for {ctx.guild.name}.')
        else:
            subs.add(user)
            await user.send(f'Hey {user.display_name}! '
                            f'You are now subscribed to DM alerts for {ctx.guild.name}.\n'
                            f'Use command \'{config.CMD_PREFIX}dm\' in the appropriate server to unsubscribe.')


def setup(client):
    client.add_cog(Info(client))
