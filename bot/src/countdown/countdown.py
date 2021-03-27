from Sessions.Session import Session
import time as t
from asyncio import sleep
from Sessions import session_manager, session_controller
from utils import player
from bot.configs import config
from discord.ext.commands import Context


# TODO make unpinned countdown embed different color!
async def cleanup_pins(ctx: Context):
    for pinned_msg in await ctx.channel.pins():
        if pinned_msg.author == config.BOT_NAME:
            await pinned_msg.unpin()


async def update_msg(session: Session):
    timer = session.timer
    timer.remaining = timer.end - t.time()
    if not session.countdown_msg:
        return
    countdown_msg = session.countdown_msg.message
    if timer.remaining < 0:
        done_msg = f'**{session.countdown_msg.title}**\nDONE!'
        await countdown_msg.edit(content=done_msg)
        for sub in session.subscribers:
            await sub.send(done_msg)
        await player.alert(session)
        await countdown_msg.unpin()
        await session_controller.end(session)
        return
    await countdown_msg.edit(content=f'**{session.countdown_msg.title}**\n'
                                     f'{timer.time_remaining_to_str(include_seconds=True)} left!')


async def start(session: Session):
    session.timer.running = True
    while True:
        time_remaining = session.timer.remaining
        await sleep(1)
        session = session_manager.active_sessions.get(session.ctx.guild.id)
        if not (session and
                session.timer.running and
                time_remaining == session.timer.remaining):
            break
        await update_msg(session)
