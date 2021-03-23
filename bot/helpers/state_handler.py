import Session

POMODORO = 'pomodoro'
SHORT_BREAK = 'short break'
LONG_BREAK = 'long break'


async def transition_session(session: Session, ctx):
    if session.state == POMODORO:
        session.pomos_completed += 1
        if session.pomos_completed % session.settings.intervals == 0:
            session.state = LONG_BREAK
        else:
            session.state = SHORT_BREAK
    else:
        session.state = POMODORO

    session.timer.calculate_delay()
    alert = f'Starting {session.timer.time_remaining_to_str(transition=True)} {session.state}.'
    await ctx.send(alert)
    for sub in session.subscribers:
        await sub.send(alert)
