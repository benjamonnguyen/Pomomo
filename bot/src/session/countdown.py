import time as t
from asyncio import sleep

from discord import Colour

from ..voice_client import vc_accessor, vc_manager
from . import session_manager, session_controller
from .Session import Session
from ..utils import player


async def handle_connection(session: Session, audio_alert: str):
    if audio_alert != 'mute':
        if not vc_accessor.get_voice_channel(session.ctx) and session.ctx.author.voice:
            if not await vc_manager.connect(session):
                print('countdown.handle_connection(): Could not connect to voice channel.')
    else:
        vc = vc_accessor.get_voice_client(session.ctx)
        if vc:
            await vc.disconnect()


async def cleanup_pins(session: Session):
    for pinned_msg in await session.ctx.channel.pins():
        if session.bot_start_msg and pinned_msg != session.bot_start_msg and pinned_msg.author == session.ctx.bot.user:
            embed = pinned_msg.embeds[0]
            embed.colour = Colour.red()
            await pinned_msg.unpin()
            await pinned_msg.edit(embed=embed)


async def update_msg(session: Session):
    timer = session.timer
    timer.remaining = timer.end - t.time()
    if not session.bot_start_msg:
        return
    countdown_msg = session.bot_start_msg
    embed = countdown_msg.embeds[0]
    if timer.remaining < 0:
        embed.colour = Colour.red()
        embed.description = 'DONE!'
        await session.auto_shush.unshush(session.ctx)
        await countdown_msg.edit(embed=embed)
        await session.dm.send_dm(embed=embed)
        await player.alert(session)
        await session_controller.end(session)
        return
    embed.description = f'{timer.time_remaining_to_str(hi_rez=True)} left!'
    await countdown_msg.edit(embed=embed)


async def start(session: Session):
    session.timer.running = True
    await cleanup_pins(session)
    while True:
        time_remaining = session.timer.remaining
        await sleep(1)
        session = session_manager.active_sessions.get(session_manager.session_id_from(session.ctx.channel))
        if not (session and
                session.timer.running and
                time_remaining == session.timer.remaining):
            break
        await update_msg(session)
