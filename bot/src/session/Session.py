from discord.ext.commands import Context
from discord import Message
from Settings import Settings
from Timer import Timer
from Stats import Stats
from subscriptions.Subscription import Subscription
from subscriptions.AutoShush import AutoShush


class Session:

    def __init__(self, state: str, settings: Settings, ctx: Context):

        self.state = state
        self.stats = Stats()
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = ctx
        # TODO store text_channel, voice_client, guild_id in place of ctx for multiple sessions per server extensibility
        # TODO In tangent with session_manager.update_ctx()
        self.timeout = 0
        self.countdown_msg = None # TODO maybe rename to start_msg?

        # Subscriptions
        self.dm = Subscription()
        self.auto_shush = AutoShush()
