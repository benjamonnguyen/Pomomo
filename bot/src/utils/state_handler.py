from Sessions.Session import Session
from configs import bot_enum


async def transition_session(session: Session):
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
    session.timer.set_time_remaining()
    alert = f'Starting {session.timer.time_remaining_to_str(singular=True)} {session.state}.'
    await session.ctx.send(alert)
    for sub in session.subscribers:
        await sub.send(alert)
