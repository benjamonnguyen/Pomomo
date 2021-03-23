import discord
import state_handler
import msg_builder
import user_messages as u_msg
import Settings
import Timer
import random


def is_connected_to_vc(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


class Session:
    # _instance = None
    #
    # def __new__(cls, pomodoro=0, short_break=0, long_break=0, intervals=0):
    #     if cls._instance is None:
    #         cls._instance = super(Session, cls).__new__(cls)
    #         cls._instance.active = False
    #     else:
    #         cls._instance.state = state.POMODORO
    #         cls._instance.pomodoro = pomodoro
    #         cls._instance.short_break = short_break
    #         cls._instance.long_break = long_break
    #         cls._instance.intervals = intervals
    #     return cls._instance
    def __init__(self, settings: Settings, vc: discord.VoiceClient):

        self.state = state_handler.POMODORO
        self.pomos_completed = 0
        self.settings = settings
        self.timer = Timer(settings.duration)
        self.vc = vc
        # self.tc = tc

    # @classmethod
    # async def valid_session_args(cls, ctx, pomodoro, short_break, long_break, intervals) -> bool:
    #     if not (pomodoro > 0 and short_break > 0 and long_break > 0 and intervals > 0):
    #         await ctx.send(u_msg.INV_NUM)
    #         return False
    #     return True

    async def send_start_msg(self, ctx):
        msg = f'{random.choice(u_msg.GREETINGS)}\n\n' + \
              msg_builder.settings_msg(self.settings)
        await ctx.send(msg)
    #
    # @classmethod
    # async def send_edit_msg(cls, ctx):
    #     await ctx.send(msg_builder.edit_msg(cls._instance.pomodoro,
    #                                         cls._instance.short_break,
    #                                         cls._instance.long_break,
    #                                         cls._instance.intervals))
    #
    # @classmethod
    # async def start(cls, ctx, timer):
    #     connected = ctx.author.voice
    #     if not connected:
    #         await ctx.send('Join a voice channel to use Pomomobot!')
    #         return
    #     vc = await connected.channel.connect()
    #     await cls._instance.send_start_msg(ctx)
    #     await timer.start(ctx, cls._instance, vc)
    #
    # @classmethod
    # async def edit(cls, ctx, timer, pomodoro, short_break, long_break, intervals):
    #     if not short_break:
    #         short_break = cls._instance.short_break
    #     if not long_break:
    #         long_break = cls._instance.long_break
    #     if not intervals:
    #         intervals = cls._instance.intervals
    #     if not await cls._instance.valid_session_args(ctx, pomodoro, short_break, long_break, intervals):
    #         return
    #
    #     cls._instance.state = state_handler.POMODORO
    #     cls._instance.pomodoro = pomodoro
    #     cls._instance.short_break = short_break
    #     cls._instance.long_break = long_break
    #     cls._instance.intervals = intervals
    #     timer.calculate_delay(cls._instance)
    #
    #     await cls._instance.send_edit_msg(ctx)
    #     await timer.start(ctx, cls._instance)
