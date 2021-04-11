from discord.ext.commands import Context

from ..Settings import Settings
from ..Stats import Stats
from ..Timer import Timer
from ..subscriptions.AutoShush import AutoShush
from ..subscriptions.Subscription import Subscription


class Session:

    def __init__(self, state: str, settings: Settings, ctx: Context):

        self.state = state
        self.settings = settings
        self.timer = Timer(self)
        self.stats = Stats()
        self.ctx = ctx
        self.timeout = 0
        self.bot_start_msg = None

        # Subscriptions
        self.dm = Subscription()
        self.auto_shush = AutoShush()
