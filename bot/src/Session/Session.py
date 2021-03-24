from Settings import Settings
from Timer import Timer
from configs import bot_enum


class Session:

    def __init__(self, settings: Settings):

        self.state = bot_enum.State.POMODORO
        self.pomos_completed = 0
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = None
        self.timeout = 0
        self.subscribers = set()
