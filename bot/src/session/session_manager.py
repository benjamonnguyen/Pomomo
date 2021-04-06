import discord
from discord.ext.commands import Context
import time as t
import asyncio
import random
from bot.configs import config, user_messages as u_msg
from session.Session import Session

active_sessions = {}


async def connect_to_voice_channel(ctx: Context):
    await ctx.author.voice.channel.connect()
    await ctx.guild.get_member(ctx.bot.user.id).edit(deafen=True)


def get_voice_client(ctx: Context):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if not (voice_client and voice_client.is_connected()):
        return
    return voice_client


def get_voice_channel(ctx: Context):
    vc = get_voice_client(ctx)
    if not vc:
        return
    return vc.channel


def get_nonbot_members_in_voice_channel(ctx: Context) -> [discord.Member]:
    vc = get_voice_channel(ctx)
    if not vc:
        return list()
    members = vc.members
    for member in members:
        if member.bot:
            members.remove(member)
    return members


async def get_server_session(ctx: Context) -> Session:
    session = active_sessions.get(ctx.guild.id)
    if session:
        session.ctx = ctx
    else:
        await ctx.send(u_msg.NO_ACTIVE_SESSION_ERR)
    return session


async def kill_if_idle(session: Session):
    ctx = session.ctx
    if not get_voice_channel(ctx) or\
            len(get_nonbot_members_in_voice_channel(ctx)) == 0:
        await ctx.invoke(ctx.bot.get_command('stop'))
        return True
    if t.time() < session.timeout:
        return
    else:
        def check(reaction, user):
            return reaction.emoji == '👍' and user != ctx.bot.user
        msg = await ctx.channel.send('Are you still there?')
        await msg.add_reaction('👍')
        try:
            await ctx.bot.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.invoke(ctx.bot.get_command('stop'))
        else:
            await ctx.send(random.choice(u_msg.STILL_THERE))
            if session.timer.running:
                session.timeout = t.time() + config.TIMEOUT
            else:
                session.timeout = t.time() + config.PAUSE_TIMEOUT
