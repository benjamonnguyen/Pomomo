from discord import FFmpegPCMAudio, PCMVolumeTransformer
import Session
import state
import config


POMO_OVER_PATH = r'sounds\pomo_end.mp3'
S_BREAK_OVER_PATH = r'sounds\break_end.mp3'
L_BREAK_ALERT_PATH = r'sounds\long_break.mp3'
FFMPEG_EXE = r'C:\ffmpeg\bin\ffmpeg.exe'


def alert(session: Session):
    if not config.voice_channel:
        return

    path = POMO_OVER_PATH
    if config.pomos_completed % session.intervals == 0:
        path = L_BREAK_ALERT_PATH
    elif session.state != state.POMODORO:
        path = S_BREAK_OVER_PATH
    source = PCMVolumeTransformer(FFmpegPCMAudio(path, executable=FFMPEG_EXE), volume=0.1)
    if config.voice_channel.is_playing():
        config.voice_channel.stop()
    config.voice_channel.play(source)
