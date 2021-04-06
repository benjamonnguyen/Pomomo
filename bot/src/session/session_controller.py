import time as t
from bot.configs import config, bot_enum
from asyncio import sleep
from utils import player
from session import session_manager, session_messenger, countdown
from session.Session import Session
from Settings import Settings
from subscriptions import auto_shush


async def resume(session: Session):  # TODO clean up method
    session.timeout = t.time() + config.TIMEOUT
    if session.state == bot_enum.State.COUNTDOWN:
        await countdown.update_msg(session)
        return
    elif session.state == bot_enum.State.POMODORO:
        await auto_shush.shush(session)
    else:
        await auto_shush.unshush(session)
    while True:
        session.timer.running = True
        timer_end = session.timer.end
        await sleep(session.timer.remaining)
        session = session_manager.active_sessions.get(session.ctx.guild.id)
        if not (session and
                session.timer.running and
                timer_end == session.timer.end):
            break
        else:
            if await session_manager.kill_if_idle(session):
                break
            if session.state == bot_enum.State.POMODORO:
                await session.subscriptions.unshush()
            await player.alert(session)
            await transition_state(session)


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
    await session.subscriptions.unshush()
    await session.subscriptions.send_dm(f'The session in {ctx.guild.name} has ended.')
    session_manager.active_sessions.pop(ctx.guild.id)


async def transition_state(session: Session):
    subs = session.subscriptions
    session.timer.running = False
    if session.state == bot_enum.State.POMODORO:
        stats = session.stats
        stats.pomos_completed += 1
        stats.minutes_completed += session.settings.duration
        if stats.pomos_completed > 0 and\
                stats.pomos_completed % session.settings.intervals == 0:
            session.state = bot_enum.State.LONG_BREAK
        else:
            session.state = bot_enum.State.SHORT_BREAK
    else:
        session.state = bot_enum.State.POMODORO
        await auto_shush.shush(session)
    session.timer.set_time_remaining()
    alert = f'Starting {session.timer.time_remaining_to_str(singular=True)} {session.state}.'
    await session.ctx.send(alert)
    await subs.send_dm(alert)
