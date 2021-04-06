from Subscriptions import Subscriptions
from discord import Embed


class DM(Subscriptions):

    def __init__(self):
        super().__init__()

    async def send_embed(self, embed: Embed):
        for sub in self.subs:
            await sub.send(embed=embed)
