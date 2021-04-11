from discord.ext import commands

from src.session import session_manager
from src.subscriptions import AutoShush
from src.voice_client import vc_accessor as vc_accessor, vc_manager as vc_manager
from configs import config, bot_enum


class Subscribe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dm(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            user = ctx.author
            subs = session.dm.subs
            if user in subs:
                subs.remove(user)
                await user.send(f'You\'ve been unsubscribed from DM alerts for {ctx.guild.name}.')
            else:
                subs.add(user)
                await user.send(f'Hey {user.display_name}! '
                                f'You are now subscribed to DM alerts for {ctx.guild.name}.\n'
                                f'Use command \'{config.CMD_PREFIX}dm\' in the text channel the session '
                                'was started from to unsubscribe.')

    @commands.command()
    async def autoshush(self, ctx, who: str = ''):
        session = await session_manager.get_session(ctx)
        if session:
            if not vc_accessor.get_voice_channel(ctx):
                await ctx.send('Pomomo must be in a voice channel to use auto-shush.')
                return
            auto_shush = session.auto_shush
            if who.lower() == AutoShush.ALL:
                await auto_shush.handle_all(ctx)
            elif ctx.author in auto_shush.subs:
                await auto_shush.remove_sub(ctx)
            else:
                await auto_shush.add_sub(session, ctx.author)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and before.channel and after.channel and before.channel.id != after.channel.id:
            session = vc_manager.get_connected_session(after.channel)
            if session:
                auto_shush = session.auto_shush
                if member in auto_shush.subs or auto_shush.all:
                    if session.state in [bot_enum.State.POMODORO, bot_enum.State.COUNTDOWN] and \
                            session.ctx.voice_client and not (member.voice.mute and member.voice.deaf):
                        await auto_shush.shush(session.ctx, member)
            elif member.voice.mute or member.voice.deaf:
                session = vc_manager.get_connected_session(before.channel)
                if session:
                    await session.auto_shush.unshush(session.ctx, member)


def setup(client):
    client.add_cog(Subscribe(client))
