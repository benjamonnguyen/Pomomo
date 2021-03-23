import discord
import Session
import Settings
import state_handler
import player
import time as t
from asyncio import sleep


class Timer:

    def __init__(self, duration: int):
        self.running = False
        self.remaining = duration * 60
        self.end = t.time() + duration * 60

    @classmethod
    def calculate_delay(cls, session: Session):
        if session.state == state_handler.POMODORO:
            cls._instance.remaining = session.duration * 60
        elif session.state == state_handler.SHORT_BREAK:
            cls._instance.remaining = session.short_break * 60
        elif session.state == state_handler.LONG_BREAK:
            cls._instance.remaining = session.long_break * 60
        cls._instance.end = t.time() + cls._instance.remaining

    @classmethod
    def get_time_remaining(cls, transition=False) -> str:
        if cls._instance.running and not transition:
            time_remaining = cls._instance.end - t.time()
        else:
            time_remaining = cls._instance.remaining
        if time_remaining < 60:
            time_string = str(int(time_remaining)) + ' second'
            if time_remaining != 1 and not transition:
                time_string += 's'
        else:
            time_string = str(int(time_remaining/60)) + ' minute'
            if time_remaining >= 120 and not transition:
                time_string += 's'
        return time_string

    @classmethod
    async def start(cls, ctx, session: Session):
        if not session.active:
            await player.alert(vc, session)
            cls._instance.calculate_delay(session)
            session.active = True
        cls._instance.running = True
        while True:
            await sleep(cls._instance.remaining)
            if not cls._instance.running:
                break
            await state_handler.handle_transition(ctx, session, cls._instance)
            await player.alert(vc, session)
