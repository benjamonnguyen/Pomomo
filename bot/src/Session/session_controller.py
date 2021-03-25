import time as t
from configs import config
from asyncio import sleep
from utils import player, state_handler
import sessions_manager
import session_messenger
from Session import Session
from Settings import Settings


async def resume(session: Session):
    session.timeout = t.time() + config.TIMEOUT
    while True:
        timer_end = session.timer.end
        await sleep(session.timer.remaining)
        session = sessions_manager.active_sessions.get(session.ctx.guild.id)
        if not (session and
                session.timer.running and
                timer_end == session.timer.end):
            break
        else:
            killed = await sessions_manager.kill_if_idle(session)
            if killed:
                break
            await player.alert(session)
            await state_handler.transition_session(session)


async def start(session: Session):
    ctx = session.ctx
    sessions_manager.active_sessions[ctx.guild.id] = session
    await session_messenger.send_start_msg(session)
    await player.alert(session)
    await resume(session)


async def edit(session: Session, new_settings: Settings):
    short_break = new_settings.short_break or session.settings.short_break
    long_break = new_settings.long_break or session.settings.long_break
    intervals = new_settings.intervals or session.settings.intervals
    session.settings = Settings(new_settings.duration, short_break, long_break, intervals)
    await session_messenger.send_edit_msg(session)
