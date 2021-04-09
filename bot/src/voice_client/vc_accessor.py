import discord
from discord.ext.commands import Context


def get_voice_client(ctx: Context):
    voice_client = ctx.voice_client
    if not (voice_client and voice_client.is_connected()):
        return
    return voice_client


def get_voice_channel(ctx: Context):
    vc = get_voice_client(ctx)
    if not vc:
        return
    return vc.channel


def get_true_members_in_voice_channel(ctx: Context) -> [discord.Member]:
    vc = get_voice_channel(ctx)
    if not vc:
        return list()
    members = vc.members
    for member in members:
        if member.bot:
            members.remove(member)
    return members


