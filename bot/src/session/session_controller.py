import time as t
from bot.configs import config, bot_enum
from asyncio import sleep
from utils import player
from session import session_manager, session_messenger, countdown, state_handler
from session.Session import Session
from Settings import Settings


async def resume(session: Session):
    session.timeout = t.time() + config.TIMEOUT_SECONDS
    await state_handler.auto_shush(session)
    if session.state == bot_enum.State.COUNTDOWN:
        await countdown.start(session)
        return
    while True:
        if not await run_interval(session):
            break


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
    await countdown.cleanup_pins(session)
    await session.auto_shush.unshush(ctx)
    for sub in session.auto_shush.subs.union(session.dm.subs):
        await sub.send(f'The session in {ctx.guild.name} has ended.')
    if session_manager.get_voice_client(ctx):
        await ctx.guild.voice_client.disconnect()
    session_manager.active_sessions.pop(ctx.guild.id)


async def run_interval(session: Session) -> bool:
    session.timer.running = True
    timer_end = session.timer.end
    await sleep(session.timer.remaining)
    session = session_manager.active_sessions.get(session.ctx.guild.id)
    if not (session and
            session.timer.running and
            timer_end == session.timer.end):
        return False
    else:
        if await session_manager.kill_if_idle(session):
            return False
        # TODO check this out, should be inside another method unless timing doesn't allow
        if session.state == bot_enum.State.POMODORO:
            await session.auto_shush.unshush(session.ctx)
        await player.alert(session)
        await state_handler.transition(session)
    return True
