from session import session_manager


class Subscriptions:

    ALL = 'all'

    def __init__(self, parent):
        self.parent = parent
        self.dm_subs = set()
        self.shush_subs = set()

    async def send_dm(self, dm: str):
        for sub in self.dm_subs:
            await sub.send(dm)

    async def shush(self, who=None):
        vc_members = session_manager.get_voice_channel_nonbot_members(self.parent.ctx)
        if who == self.ALL:
            for member in vc_members:
                await member.edit(deafen=True, mute=True)
        elif who:
            await who.edit(deafen=True, mute=True)
        elif self.ALL in self.shush_subs:
            for member in vc_members:
                await member.edit(deafen=True, mute=True)
        else:
            for member in vc_members:
                if member in self.shush_subs:
                    await member.edit(deafen=True, mute=True)

    async def unshush(self, who=None):
        vc_members = session_manager.get_voice_channel_nonbot_members(self.parent.ctx)
        if who == self.ALL:
            for member in vc_members:
                await member.edit(deafen=False, mute=False)
        elif who:
            await who.edit(deafen=False, mute=False)
        elif self.ALL in self.shush_subs:
            for member in vc_members:
                await member.edit(deafen=False, mute=False)
        else:
            for member in vc_members:
                if member in self.shush_subs:
                    await member.edit(deafen=False, mute=False)
