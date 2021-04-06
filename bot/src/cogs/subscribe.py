import discord
from discord.ext import commands
from session import session_manager
from bot.configs import config, bot_enum
from subscriptions import auto_shush


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
                                f'Use command \'{config.CMD_PREFIX}dm\' in one of the server\'s '
                                'text channels to unsubscribe.')

    @commands.command()
    async def auto_shush(self, ctx, who: str = ''):
        session = await session_manager.get_server_session(ctx)
        if session:
            if session.state == bot_enum.State.COUNTDOWN:
                await ctx.send('Auto-shush only works with pomodoro sessions.')
                return
            user = ctx.author
            subs = session.subscriptions.shush_subs
            vc_members = session_manager.get_nonbot_members_in_voice_channel(ctx)
            vc_name = session_manager.get_voice_channel(ctx).name
            if who.lower() == auto_shush.ALL:
                permissions = user.permissions_in(ctx.channel)
                if not ((permissions.deafen_members and permissions.mute_members) or permissions.administrator):
                    await ctx.send('You do not have permission to mute and deafen other members.')
                    return
                if auto_shush.ALL in subs:
                    subs.remove(auto_shush.ALL)
                    await ctx.send(f'Auto-shush has been turned off for the {vc_name} channel.')
                    await session.subscriptions.unshush(auto_shush.ALL)
                else:
                    subs.add(auto_shush.ALL)
                    await ctx.send(f'Auto-shush has been turned on for the {vc_name} channel.')
                    await auto_shush.shush(session)
            elif user in subs:
                if auto_shush.ALL in subs:
                    await ctx.send(f'Auto-shush is already turned on for all members in the {vc_name} channel.')
                    return
                if user in vc_members:
                    subs.remove(user)
                    await auto_shush.unshush(session)
                    await user.send('You will no longer be automatically deafened and muted'
                                    f' during pomodoro intervals in {ctx.guild.name}\'s '
                                    f'{vc_name} channel.\n')
            else:
                if auto_shush.ALL in subs:
                    await ctx.send(f'Auto-shush is already turned on for all members in the {vc_name} channel.')
                    return
                if session.state == bot_enum.State.POMODORO and user in vc_members:
                    subs.add(user)
                    await auto_shush.shush(session, user)
                    await user.send(f'Hey {user.display_name}! '
                                    'You will now be automatically deafened and muted '
                                    f'during pomodoro intervals in {ctx.guild.name}\'s {vc_name} channel.\n'
                                    f'Use command \'{config.CMD_PREFIX}auto_shush\' in one of the server\'s '
                                    'text channels to turn off auto-shush.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and before and after and before.channel.id != after.channel.id:
            session = session_manager.active_sessions.get(member.guild.id)
            if not session:
                return
            subs = session.subscriptions.shush_subs
            if member in subs or auto_shush.ALL in subs:
                voice_client = discord.utils.get(self.client.voice_clients, guild=member.guild)
                if after.channel.id == voice_client.channel.id:
                    if not(member.voice.mute and member.voice.deaf):
                        await auto_shush.shush(session, member)
                elif member.voice.mute and member.voice.deaf and before.channel.id == voice_client.channel.id:
                    await auto_shush.unshush(session, member)


def setup(client):
    client.add_cog(Subscribe(client))
