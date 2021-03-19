import Session
import Timer
import config

POMODORO = 'pomodoro'
SHORT_BREAK = 'short break'
LONG_BREAK = 'long break'


async def handle_transition(ctx, session: Session, timer: Timer):
    if session.state == POMODORO:
        config.pomos_completed += 1
        if config.pomos_completed % session.intervals == 0:
            session.state = LONG_BREAK
        else:
            session.state = SHORT_BREAK
    else:
        session.state = POMODORO

    timer.calculate_delay(session)
    time_remaining = timer.calculate_time_remaining()
    await ctx.send(f'Starting {time_remaining} {session.state}.')
