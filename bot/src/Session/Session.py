from Settings import Settings
from Timer import Timer
from Stats import Stats
from configs import bot_enum


class Session:

    def __init__(self, settings: Settings):

        self.state = bot_enum.State.POMODORO
        self.stats = Stats()
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = None
        self.timeout = 0
        self.subscribers = set()
