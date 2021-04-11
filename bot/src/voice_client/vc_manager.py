from discord import VoiceChannel

from configs import user_messages as u_msg
from ..session.Session import Session

connected_sessions = {}


async def connect(session: Session):
    ctx = session.ctx
    if ctx.voice_client and get_connected_session(ctx.voice_client.channel):
        await ctx.send(u_msg.ACTIVE_SESSION_EXISTS_ERR)
        return
    voice_client = await ctx.author.voice.channel.connect()
    await ctx.guild.get_member(ctx.bot.user.id).edit(deafen=True)
    if voice_client:
        connected_sessions[voice_channel_id_from(voice_client.channel)] = session
    return True


async def disconnect(session: Session):
    vc_id = voice_channel_id_from(session.ctx.voice_client.channel)
    await session.ctx.voice_client.disconnect()
    connected_sessions.pop(vc_id)


def get_connected_session(vc: VoiceChannel) -> Session:
    return connected_sessions.get(voice_channel_id_from(vc))


def voice_channel_id_from(vc: VoiceChannel) -> str:
    return str(vc.guild.id) + str(vc.id)
