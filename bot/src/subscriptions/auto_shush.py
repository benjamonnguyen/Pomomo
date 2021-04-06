from session import session_manager


ALL = 'all'


async def shush(session, who=None):
    vc_members = session_manager.get_nonbot_members_in_voice_channel(session.ctx)
    if who == ALL:
        for member in vc_members:
            await member.edit(deafen=True, mute=True)
    elif who:
        await who.edit(deafen=True, mute=True)
    elif ALL in session.subscriptions.shush_subs:
        for member in vc_members:
            await member.edit(deafen=True, mute=True)
    else:
        for member in vc_members:
            if member in session.subscriptions.shush_subs:
                await member.edit(deafen=True, mute=True)


async def unshush(session, who=None):
    vc_members = session_manager.get_nonbot_members_in_voice_channel(session.ctx)
    if who == ALL:
        for member in vc_members:
            await member.edit(deafen=False, mute=False)
    elif who:
        await who.edit(deafen=False, mute=False)
    elif ALL in session.subscriptions.shush_subs:
        for member in vc_members:
            await member.edit(deafen=False, mute=False)
    else:
        for member in vc_members:
            if member in session.subscriptions.shush_subs:
                await member.edit(deafen=False, mute=False)
