import Session
import Timer

POMODORO = 'pomodoro'
SHORT_BREAK = 'short break'
LONG_BREAK = 'long break'


async def handle_transition(ctx, session: Session, timer: Timer):
    if session.state == POMODORO:
        session.pomos_completed += 1
        if session.pomos_completed % session.intervals == 0:
            session.state = LONG_BREAK
        else:
            session.state = SHORT_BREAK
    else:
        session.state = POMODORO

    timer.calculate_delay(session)
    time_remaining = timer.get_time_remaining(transition=True)
    await ctx.send(f'Starting {time_remaining} {session.state}.')
