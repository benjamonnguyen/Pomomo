import state, msg_builder as msg
import config


class Session:
    _instance = None

    def __new__(cls, duration=0, short_break=0, long_break=0, intervals=0):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.active = False
        else:
            cls._instance.state = state.POMODORO
            cls._instance.duration = duration
            cls._instance.short_break = short_break
            cls._instance.long_break = long_break
            cls._instance.intervals = intervals
        return cls._instance

    @classmethod
    async def valid_session_args(cls, ctx, duration, short_break, long_break, intervals) -> bool:
        if not (duration > 0 and short_break > 0 and long_break > 0 and intervals > 0):
            await ctx.send('Must use numbers greater than 0.')
            return False
        return True

    @classmethod
    async def send_start_msg(cls, ctx):
        start_msg = msg.build_start_msg(cls._instance.duration,
                                        cls._instance.short_break,
                                        cls._instance.long_break,
                                        cls._instance.intervals)
        await ctx.send(start_msg)

    @classmethod
    async def send_edit_msg(cls, ctx):
        edit_msg = msg.build_edit_msg(cls._instance.duration,
                                        cls._instance.short_break,
                                        cls._instance.long_break,
                                        cls._instance.intervals)
        await ctx.send(edit_msg)

    @classmethod
    async def start(cls, ctx, timer):
        connected = ctx.author.voice
        if not connected:
            await ctx.send('Join a voice channel to use Pomomobot!')
            return
        config.voice_channel = await connected.channel.connect()
        await cls._instance.send_start_msg(ctx)
        await timer.start(ctx, cls._instance)

    @classmethod
    async def edit(cls, ctx, timer, duration, short_break, long_break, intervals):
        if not short_break:
            short_break = cls._instance.short_break
        if not long_break:
            long_break = cls._instance.long_break
        if not intervals:
            intervals = cls._instance.intervals
        if not await cls._instance.valid_session_args(ctx, duration, short_break, long_break, intervals):
            return

        cls._instance.state = state.POMODORO
        cls._instance.duration = duration
        cls._instance.short_break = short_break
        cls._instance.long_break = long_break
        cls._instance.intervals = intervals
        timer.calculate_delay(cls._instance)

        await cls._instance.send_edit_msg(ctx)
        await timer.start(ctx, cls._instance)

