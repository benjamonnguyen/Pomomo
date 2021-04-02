import discord
from discord.ext.commands import Context
import time as t
import asyncio
import random
from bot.configs import config, user_messages as u_msg
from session.Session import Session

active_sessions = {}


def connected_to_vc(ctx: Context):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


async def get_server_session(ctx: Context) -> Session:
    session = active_sessions.get(ctx.guild.id)
    if session:
        session.ctx = ctx
    else:
        await ctx.send(u_msg.NO_ACTIVE_SESSION_ERR)
    return session


async def kill_if_idle(session: Session):
    ctx = session.ctx
    if not connected_to_vc(ctx) or\
            len(ctx.voice_client.channel.members) < 2:
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
