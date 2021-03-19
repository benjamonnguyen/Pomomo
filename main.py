import os
from dotenv import load_dotenv
from discord.ext import commands
import time as t
import msg_builder as msg
import state
import config
import Timer, Session

ERROR_CODE = 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='pom!', help_command=None)
timer = Timer.Timer()
session = Session.Session()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command(pass_context=True)
async def help(ctx, command=''):
    help_msg = msg.build_help_msg(command)
    await ctx.send(help_msg)


@client.command(pass_context=True)
async def start(ctx, duration=20, short_break=5, long_break=15, intervals=4):
    global session
    global timer

    if session.active:
        await ctx.send(msg.ACTIVE_SESSION)
        return
    if not await session.valid_session_args(ctx, duration, short_break, long_break, intervals):
        return

    session = Session.Session(duration, short_break, long_break, intervals)
    timer = Timer.Timer()
    config.pomos_completed = 0
    await session.start(ctx, timer)


@start.error
async def handle_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Must use numbers greater than 0.')
    else:
        print(error)


@client.command(pass_context=True)
async def stop(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
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


@client.command(pass_context=True)
async def pause(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return
    if not timer.running:
        await ctx.send('Timer is already paused.')
        return

    timer.running = False
    timer.remaining = timer.end - t.time()
    await ctx.send(f'Pausing {session.state}.')


@client.command(pass_context=True)
async def resume(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return
    if timer.running:
        await ctx.send('Timer is already running.')
        await ctx.invoke(client.get_command('time'))
        return

    timer.end = t.time() + timer.remaining
    await ctx.send(f'Resuming {session.state}.')
    await timer.start(ctx, session)


@client.command(pass_context=True)
async def restart(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return

    timer.calculate_delay(session)
    await ctx.send(f'Restarting {session.state}.')
    await timer.start(ctx, session)


@client.command(pass_context=True)
async def skip(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return

    if config.pomos_completed > 0 and session.state == state.POMODORO:
        config.pomos_completed -= 1

    await ctx.send(f'Skipping {session.state}.')
    await state.handle_transition(ctx, session, timer)
    await timer.start(ctx, session)


@client.command(pass_context=True)
async def time(ctx):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return

    time_remaining = timer.calculate_time_remaining()
    await ctx.send(f'{time_remaining} remaining on {session.state}!')


@client.command(pass_context=True)
async def edit(ctx, duration: int, short_break: int = None, long_break: int = None, intervals: int = None):
    global session
    global timer

    if not session.active:
        await ctx.send(msg.NO_ACTIVE_SESSION)
        return

    await session.edit(ctx, timer, duration, short_break, long_break, intervals)


@edit.error
async def handle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Pass in at least one number.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Must use numbers greater than 0.')
    else:
        print(error)


@client.command(pass_context=True)
async def begone(ctx):
    if ctx.voice_client:
        if str(ctx.message.author) != 'elisetnguyen8#8122':
            await ctx.send("Nah...you begone THOT!")
        else:
            await ctx.send(f'Hi Elise! Looking cute today ;)')
            await ctx.guild.voice_client.disconnect()


client.run(TOKEN)
