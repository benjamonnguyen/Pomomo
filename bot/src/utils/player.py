from asyncio import sleep

from discord import FFmpegPCMAudio, PCMVolumeTransformer

from configs import bot_enum
from ..session.Session import Session


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
