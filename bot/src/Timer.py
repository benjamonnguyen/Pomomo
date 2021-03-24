from configs import bot_enum
import time as t


class Timer:

    def __init__(self, parent):
        duration = parent.settings.duration * 60
        self.parent = parent
        self.running = False
        self.remaining = duration
        self.end = t.time() + duration

    def calculate_delay(self):
        session = self.parent
        if session.state == bot_enum.State.POMODORO:
            delay = session.settings.duration * 60
        elif session.state == bot_enum.State.SHORT_BREAK:
            delay = session.settings.short_break * 60
        elif self.parent.state == bot_enum.State.LONG_BREAK:
            delay = session.settings.long_break * 60
        else:
            raise Exception('No valid session state: ' + session.state)
        self.remaining = delay
        self.end = t.time() + delay

    def time_remaining_to_str(self, singular=False) -> str:
        if self.running and not singular:
            time_remaining = self.end - t.time()
        else:
            time_remaining = self.remaining
        if time_remaining < 60:
            time_string = str(int(time_remaining)) + ' second'
            if time_remaining != 1 and not singular:
                time_string += 's'
        else:
            time_string = str(int(time_remaining/60)) + ' minute'
            if time_remaining >= 120 and not singular:
                time_string += 's'
        return time_string
