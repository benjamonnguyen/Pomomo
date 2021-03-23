from discord import FFmpegPCMAudio, PCMVolumeTransformer
import Session
import state_handler
from asyncio import sleep


POMO_OVER_PATH = '../sounds/pomo_end.mp3'
S_BREAK_OVER_PATH = '../sounds/break_end.mp3'
L_BREAK_ALERT_PATH = '../sounds/long_break.mp3'


async def alert(session: Session):
    vc = session.ctx.voice_client
    if not vc:
        return

    path = POMO_OVER_PATH
    if session.pomos_completed % session.settings.intervals == 0:
        path = L_BREAK_ALERT_PATH
    elif session.state != state_handler.POMODORO:
        path = S_BREAK_OVER_PATH
    source = PCMVolumeTransformer(FFmpegPCMAudio(path, executable='../sounds/ffmpeg.exe'),
                                  volume=0.1)
    if vc.is_playing():
        vc.stop()
    vc.play(source)
    while vc.is_playing():
        await sleep(1)
