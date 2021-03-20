from discord.ext import commands
import time as t
import msg_builder
import user_messages as u_msg
import state
import config
import Timer, Session

timer = Timer.Timer()
session = Session.Session()


class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def help(self, ctx, command=''):
        await ctx.send(msg_builder.help_msg(command))

    @commands.command(pass_context=True)
    async def start(self, ctx, duration=20, short_break=5, long_break=15, intervals=4):
        global session
        global timer

        if session.active:
            await ctx.send(u_msg.ACTIVE_SESSION)
            return
        if not await session.valid_session_args(ctx, duration, short_break, long_break, intervals):
            return

        session = Session.Session(duration, short_break, long_break, intervals)
        timer = Timer.Timer()
        config.pomos_completed = 0
        await session.start(ctx, timer)

    @start.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.INV_NUM)
        else:
            print(error)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            if config.pomos_completed > 0:
                await ctx.send(f'Great job! You completed {config.pomos_completed} pomodoros.')
            else:
                await ctx.send(f'See you again soon!')
        session.active = False
        timer.running = False
        config.voice_channel = None

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return
        if not timer.running:
            await ctx.send('Timer is already paused.')
            return

        timer.running = False
        timer.remaining = timer.end - t.time()
        await ctx.send(f'Pausing {session.state}.')

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return
        if timer.running:
            await ctx.send('Timer is already running.')
            await ctx.invoke(client.get_command('time'))
            return

        timer.end = t.time() + timer.remaining
        await ctx.send(f'Resuming {session.state}.')
        await timer.start(ctx, session)

    @commands.command(pass_context=True)
    async def restart(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        timer.calculate_delay(session)
        await ctx.send(f'Restarting {session.state}.')
        await timer.start(ctx, session)

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        if config.pomos_completed > 0 and session.state == state.POMODORO:
            config.pomos_completed -= 1

        await ctx.send(f'Skipping {session.state}.')
        await state.handle_transition(ctx, session, timer)
        await timer.start(ctx, session)

    @commands.command(pass_context=True)
    async def time(self, ctx):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        time_remaining = timer.calculate_time_remaining()
        await ctx.send(f'{time_remaining} remaining on {session.state}!')

    @commands.command(pass_context=True)
    async def edit(self, ctx, duration: int, short_break: int = None, long_break: int = None, intervals: int = None):
        global session
        global timer

        if not session.active:
            await ctx.send(u_msg.NO_ACTIVE_SESSION)
            return

        await session.edit(ctx, timer, duration, short_break, long_break, intervals)

    @edit.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Pass in at least one number.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.INV_NUM)
        else:
            print(error)


def setup(client):
    client.add_cog(Command(client))
