from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext.commands import Context
import Session
from bot.configs import bot_enum
from Sessions import session_manager
from asyncio import sleep


async def alert(session: Session):
    vc = session.ctx.voice_client
    if not vc:
        return

    path = bot_enum.AlertPath.POMO_END
    if session.state == bot_enum.State.COUNTDOWN:
        pass
    elif session.stats.pomos_completed % session.settings.intervals == 0:
        path = bot_enum.AlertPath.LONG_BREAK_START
    elif session.state != bot_enum.State.POMODORO:
        path = bot_enum.AlertPath.POMO_START
    source = PCMVolumeTransformer(FFmpegPCMAudio(path, executable='../sounds/ffmpeg.exe'),
                                  volume=0.1)
    if vc.is_playing():
        vc.stop()
    vc.play(source)
    while vc.is_playing():
        await sleep(1)


async def setup_countdown(ctx: Context, audio_alert: bool):
    if audio_alert:
        if not session_manager.connected_to_vc(ctx):
            await ctx.author.voice.channel.connect()
    else:
        if session_manager.connected_to_vc(ctx):
            await ctx.guild.voice_client.disconnect()
