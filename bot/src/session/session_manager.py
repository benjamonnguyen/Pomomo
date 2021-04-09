from discord.ext.commands import Context
from discord import TextChannel
import time as t
import asyncio
import random
from bot.configs import config, user_messages as u_msg
from session.Session import Session
from vc_accessor import get_voice_channel, get_true_members_in_voice_channel

active_sessions = {}


def activate(session: Session):
    active_sessions[session_id_from(session.ctx.channel)] = session


def deactivate(session: Session):
    active_sessions.pop(session_id_from(session.ctx.channel))


async def get_session(ctx: Context) -> Session:
    session = active_sessions.get(session_id_from(ctx.channel))
    if not session:
        await ctx.send(u_msg.NO_ACTIVE_SESSION_ERR)
    return session


def session_id_from(tc: TextChannel) -> str:
    return str(tc.guild.id) + str(tc.id)


async def kill_if_idle(session: Session):
    ctx = session.ctx
    if not get_voice_channel(ctx) or\
            len(get_true_members_in_voice_channel(ctx)) == 0:
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
                session.timeout = t.time() + config.TIMEOUT_SECONDS
            else:
                session.timeout = t.time() + config.PAUSE_TIMEOUT_SECONDS
