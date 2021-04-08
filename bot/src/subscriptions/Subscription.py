from discord import Embed


class Subscription:

    def __init__(self):
        self.subs = set()

    async def send_dm(self, content: str = None, embed: Embed = None):
        if content or embed:
            for sub in self.subs:
                await sub.send(content=content, embed=embed)
        else:
            raise Exception('No arguments passed.')
