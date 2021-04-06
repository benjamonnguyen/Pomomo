from discord.ext.commands import Context
from discord import Message
from Settings import Settings
from Timer import Timer
from Stats import Stats
from subscriptions.DM import DM
from subscriptions.AutoShush import AutoShush


class Session:

    def __init__(self, state: str, settings: Settings, ctx: Context):

        self.state = state
        self.stats = Stats()
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = ctx
        self.timeout = 0
        self.dm = DM()
        self.auto_shush = AutoShush()

        self.countdown_msg: Message
