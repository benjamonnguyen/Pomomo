from configs import user_messages as u_msg, config


class Settings:

    def __init__(self, duration, short_break=None, long_break=None, intervals=None):
        self.duration = duration
        self.short_break = short_break
        self.long_break = long_break
        self.intervals = intervals

    @classmethod
    async def is_valid(cls, ctx, duration: int, short_break: int = None,
                       long_break: int = None, intervals: int = None) -> bool:
        if config.MAX_INTERVAL_MINUTES > duration > 0 \
                and (not short_break or config.MAX_INTERVAL_MINUTES > short_break > 0) \
                and (not long_break or config.MAX_INTERVAL_MINUTES > long_break > 0) \
                and (not intervals or config.MAX_INTERVAL_MINUTES > intervals > 0):
            return True
        await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        return False
