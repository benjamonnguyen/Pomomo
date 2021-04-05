from discord.ext.commands import Context
from discord import Message
from Settings import Settings
from Timer import Timer
from Stats import Stats
from Subscriptions import Subscriptions


class Session:

    def __init__(self, state: str, settings: Settings, ctx: Context):

        self.state = state
        self.stats = Stats()
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = ctx
        self.timeout = 0
        self.subscriptions = Subscriptions(self)

        self.countdown_msg: Message
