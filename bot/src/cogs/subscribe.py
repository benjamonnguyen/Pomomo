import discord
from discord.ext import commands
from session import session_manager
from bot.configs import config, bot_enum
from subscriptions import AutoShush


class Subscribe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dm(self, ctx):
        session = await session_manager.get_server_session(ctx)
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
                                f'Use command \'{config.CMD_PREFIX}dm\' in one of the server\'s '
                                'text channels to unsubscribe.')

    @commands.command()
    async def autoshush(self, ctx, who: str = ''):
        session = await session_manager.get_server_session(ctx)
        if session:
            if not session_manager.get_voice_channel(ctx):
                await ctx.send('Pomomo must be in a voice channel to use auto-shush.')
                return
            auto_shush = session.auto_shush
            if who.lower() == AutoShush.ALL:
                await auto_shush.handle_all(ctx)
            elif ctx.author in auto_shush.subs:
                await auto_shush.remove_sub(ctx)
            else:
                await auto_shush.add_sub(session.state, ctx)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and before.channel and after.channel and before.channel.id != after.channel.id:
            session = session_manager.active_sessions.get(member.guild.id)
            if session:
                auto_shush = session.auto_shush
                if member in auto_shush.subs or auto_shush.all:
                    voice_client = discord.utils.get(self.client.voice_clients, guild=member.guild)
                    if session.state in [bot_enum.State.POMODORO, bot_enum.State.COUNTDOWN] and after.channel.id == \
                            voice_client.channel.id and not (member.voice.mute and member.voice.deaf):
                        await auto_shush.shush(session.ctx, member)
                    elif (member.voice.mute or member.voice.deaf) and before.channel.id == voice_client.channel.id:
                        await auto_shush.unshush(session.ctx, member)


def setup(client):
    client.add_cog(Subscribe(client))
