def is_valid(pomodoro: int, short_break: int, long_break: int, intervals: int) -> bool:
    if pomodoro > 0 and short_break > 0 \
            and long_break > 0 and intervals > 0:
        return True
    return False


class Settings:
    def __init__(self, duration, short_break, long_break, intervals):
        self.duration = duration
        self.short_break = short_break
        self.long_break = long_break
        self.intervals = intervals
