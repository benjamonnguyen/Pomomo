import user_messages as u_msg


class Settings:

    def __init__(self, duration, short_break=None, long_break=None, intervals=None):
        self.duration = duration
        self.short_break = short_break
        self.long_break = long_break
        self.intervals = intervals

    @classmethod
    async def is_valid(cls, ctx, duration: int, short_break: int = None,
                       long_break: int = None, intervals: int = None) -> bool:
        if duration > 0 and (not short_break or short_break > 0) \
                and (not long_break or long_break > 0) and (not intervals or intervals > 0):
            return True
        await ctx.send(u_msg.NUM_LT_ONE_ERR)
        return False
