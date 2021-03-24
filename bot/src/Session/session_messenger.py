import random
from utils import msg_builder
from configs import user_messages as u_msg


async def send_start_msg(session):
    msg = f'{random.choice(u_msg.GREETINGS)}\n\n' + \
          msg_builder.settings_msg(session.settings)
    await session.ctx.send(msg)


async def send_edit_msg(session):
    msg = 'Continuing pomodoro session with new settings!\n\n' + \
          msg_builder.settings_msg(session.settings)
    await session.ctx.send(msg)
