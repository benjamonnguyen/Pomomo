from discord.ext import commands
from Sessions import session_manager, session_controller, session_messenger
from Sessions.Session import Session
from Settings import Settings
from utils import state_handler, msg_builder, player
from bot.configs import config, bot_enum, user_messages as u_msg
import time as t
from countdown import countdown


class Control(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx, pomodoro=20, short_break=5, long_break=15, intervals=4):
        if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
            return

        if session_manager.connected_to_vc(ctx):
            await ctx.send(u_msg.ACTIVE_SESSION_EXISTS_ERR)
            return
        if not ctx.author.voice:
            await ctx.send('Join a voice channel to use Pomomo!')
            return
        await ctx.author.voice.channel.connect()

        session = Session(bot_enum.State.POMODORO,
                          Settings(pomodoro, short_break, long_break, intervals),
                          ctx)
        await session_controller.start(session)

    @start.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_LT_ONE_ERR)
        else:
            raise error

    @commands.command()
    async def stop(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            await session_controller.end(session)
            if session.stats.pomos_completed > 0:
                await ctx.send(f'Great job! '
                               f'You completed {msg_builder.stats_msg(session.stats)}.')
            else:
                await ctx.send(f'See you again soon! 👋')

    @commands.command()
    async def pause(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            timer = session.timer
            if not timer.running:
                await ctx.send('Timer is already paused.')
                return

            timer.running = False
            timer.remaining = timer.end - t.time()
            await ctx.send(f'Pausing {session.state}.')
            session.timeout = t.time() + config.PAUSE_TIMEOUT

    @commands.command()
    async def resume(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            timer = session.timer
            if session.timer.running:
                await ctx.send('Timer is already running.')
                return

            timer.running = True
            timer.end = t.time() + timer.remaining
            await ctx.send(f'Resuming {session.state}.')
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.start(session)
            else:
                await session_controller.resume(session)

    @commands.command()
    async def restart(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session:
            session.timer.set_time_remaining()
            await ctx.send(f'Restarting {session.state}.')
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.start(session)
            else:
                await session_controller.resume(session)

    @commands.command()
    async def skip(self, ctx):
        session = await session_manager.get_server_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Countdowns cannot be skipped. '
                     f'Use {config.CMD_PREFIX}stop to end or {config.CMD_PREFIX}restart to start over.')
        if session:
            stats = session.stats
            if stats.pomos_completed >= 0 and \
                    session.state == bot_enum.State.POMODORO:
                stats.pomos_completed -= 1
                stats.minutes_completed -= session.settings.duration

            await ctx.send(f'Skipping {session.state}.')
            await state_handler.transition_session(session)
            await session_controller.resume(session)

    @commands.command()
    async def edit(self, ctx, pomodoro: int, short_break: int = None, long_break: int = None, intervals: int = None):
        session = await session_manager.get_server_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Countdowns cannot be edited. '
                     f'Use {config.CMD_PREFIX}countdown to start a new one.')
        if session:
            if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
                return
            await session_controller.edit(session, Settings(pomodoro, short_break, long_break, intervals))
            session.timer.set_time_remaining()
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.update_msg(session)
            await session_controller.resume(session)

    @edit.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_LT_ONE_ERR)
        else:
            raise error

    @commands.command()
    async def countdown(self, ctx, duration: int, title='Countdown', audio_alert=True):
        session = session_manager.active_sessions.get(ctx.guild.id)
        if session:
            await ctx.send('There is an active session running. '
                           'Are you sure you want to start a countdown? (y/n)')
            response = await self.client.wait_for('message', timeout=60)
            if not response.content.lower()[0] == 'y':
                await ctx.send('OK, cancelling new countdown.')
                return

        if not 0 < duration <= 60:
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_SIXTY_ERR)
        await player.setup_countdown(ctx, audio_alert)
        session = Session(bot_enum.State.COUNTDOWN,
                          Settings(duration),
                          ctx)
        session_manager.active_sessions[session.ctx.guild.id] = session
        await session_messenger.send_countdown_msg(session, title)
        await countdown.start(session)

    @countdown.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_SIXTY_ERR)
        else:
            raise error


def setup(client):
    client.add_cog(Control(client))
