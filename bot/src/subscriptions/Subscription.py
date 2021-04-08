class Subscription:

    def __init__(self):
        self.subs = set()

    async def send_dm(self, dm: str):
        for sub in self.subs:
            await sub.send(dm)
