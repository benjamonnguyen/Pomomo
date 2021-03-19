import Session
import state, player
import time as t
from asyncio import sleep


class Timer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Timer, cls).__new__(cls)
            cls._instance.end = 0
            cls._instance.remaining = 0
            cls._instance.running = False
        return cls._instance

    @classmethod
    def calculate_delay(cls, session: Session):
        if session.state == state.POMODORO:
            cls._instance.remaining = session.duration * 60
        elif session.state == state.SHORT_BREAK:
            cls._instance.remaining = session.short_break * 60
        elif session.state == state.LONG_BREAK:
            cls._instance.remaining = session.long_break * 60
        cls._instance.end = t.time() + cls._instance.remaining

    @classmethod
    def calculate_time_remaining(cls) -> str:
        if cls._instance.running:
            time_remaining = cls._instance.end - t.time()
        else:
            time_remaining = cls._instance.remaining
        if time_remaining < 60:
            time_string = str(int(time_remaining)) + ' second'
            if time_remaining != 1:
                time_string += 's'
        else:
            time_string = str(int(time_remaining/60)) + ' minute'
            if time_remaining >= 120:
                time_string += 's'
        return time_string

    @classmethod
    async def start(cls, ctx, session: Session):
        if not session.active:
            player.alert(session)
            cls._instance.calculate_delay(session)
            session.active = True
        cls._instance.running = True
        while True:
            await sleep(cls._instance.remaining)
            if not cls._instance.running:
                break
            await state.handle_transition(ctx, session, cls._instance)
            player.alert(session)
