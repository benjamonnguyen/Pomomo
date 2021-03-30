from bot.configs import bot_enum
import time as t


class Timer:

    def __init__(self, parent):
        duration = parent.settings.duration * 60
        self.parent = parent
        self.running = False
        self.remaining = duration
        self.end = t.time() + duration

    def set_time_remaining(self):
        session = self.parent
        if session.state == bot_enum.State.SHORT_BREAK:
            delay = session.settings.short_break * 60
        elif self.parent.state == bot_enum.State.LONG_BREAK:
            delay = session.settings.long_break * 60
        else:
            delay = session.settings.duration * 60
        self.remaining = delay
        self.end = t.time() + delay

    def time_remaining_to_str(self, singular=False, include_seconds=False) -> str:
        if self.running:  # and not singular???
            time_remaining = self.end - t.time()
        else:
            time_remaining = self.remaining

        if time_remaining > 59:
            minutes_str = str(int(time_remaining/60)) + ' minute'
            if time_remaining >= 120 and not singular:
                minutes_str += 's'
            time_remaining_str = minutes_str
        if time_remaining < 60:
            seconds_str = str(int(time_remaining)) + ' second'
            if time_remaining >= 2 and not singular:
                seconds_str += 's'
            time_remaining_str = seconds_str
        elif include_seconds:
            seconds_str = str(int(time_remaining) % 60) + ' second'
            if time_remaining % 60 >= 2 and not singular:
                seconds_str += 's'
            time_remaining_str += ' ' + seconds_str

        return time_remaining_str
