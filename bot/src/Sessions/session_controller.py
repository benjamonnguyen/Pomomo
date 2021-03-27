import time as t
from bot.configs import config, bot_enum
from asyncio import sleep
from utils import player, state_handler
from Sessions import session_manager, session_messenger
from Sessions.Session import Session
from Settings import Settings
from countdown import countdown


async def resume(session: Session):
    session.timeout = t.time() + config.TIMEOUT
    if session.state == bot_enum.State.COUNTDOWN:
        await countdown.update_msg(session)
        return
    session.timer.running = True
    while True:
        timer_end = session.timer.end
        await sleep(session.timer.remaining)
        session = session_manager.active_sessions.get(session.ctx.guild.id)
        if not (session and
                session.timer.running and
                timer_end == session.timer.end):
            break
        else:
            killed = await session_manager.kill_if_idle(session)
            if killed:
                break
            await player.alert(session)
            await state_handler.transition_session(session)


async def start(session: Session):
    session_manager.active_sessions[session.ctx.guild.id] = session
    await session_messenger.send_start_msg(session)
    await player.alert(session)
    await resume(session)


async def edit(session: Session, new_settings: Settings):
    short_break = new_settings.short_break or session.settings.short_break
    long_break = new_settings.long_break or session.settings.long_break
    intervals = new_settings.intervals or session.settings.intervals
    session.settings = Settings(new_settings.duration, short_break, long_break, intervals)
    await session_messenger.send_edit_msg(session)


async def end(session: Session):
    ctx = session.ctx
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    await countdown.cleanup_pins(ctx)
    session_manager.active_sessions.pop(ctx.guild.id)
