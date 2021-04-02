class Subscriptions:

    def __init__(self):
        self.dm_subs = set()
        self.shush_subs = set()

    async def send_dm(self, dm: str):
        for sub in self.dm_subs:
            await sub.send(dm)

    async def shush(self):
        for sub in self.shush_subs:
            await sub.edit(deafen=True, mute=True)

    async def unshush(self):
        for sub in self.shush_subs:
            await sub.edit(deafen=False, mute=False)
