from Session import Session
from configs import bot_enum


async def transition_session(session: Session):
    if session.state == bot_enum.State.POMODORO:
        session.pomos_completed += 1
        if session.pomos_completed % session.settings.intervals == 0:
            session.state = bot_enum.State.LONG_BREAK
        else:
            session.state = bot_enum.State.SHORT_BREAK
    else:
        session.state = bot_enum.State.POMODORO

    session.timer.calculate_delay()
    alert = f'Starting {session.timer.time_remaining_to_str(singular=True)} {session.state}.'
    await session.ctx.send(alert)
    for sub in session.subscribers:
        await sub.send(alert)
