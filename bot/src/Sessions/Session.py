from discord.ext.commands import Context
from Settings import Settings
from Timer import Timer
from Stats import Stats


class Session:

    def __init__(self, state: str, settings: Settings, ctx: Context):

        self.state = state
        self.stats = Stats()
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = ctx
        self.timeout = 0
        self.subscribers = set()

        self.countdown_msg = None
