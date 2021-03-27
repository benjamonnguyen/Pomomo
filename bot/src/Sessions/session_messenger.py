import random
from utils import msg_builder
from bot.configs import user_messages as u_msg
from Sessions.Session import Session
from countdown.CountdownMsg import CountdownMsg


async def send_start_msg(session: Session):
    msg = f'{random.choice(u_msg.GREETINGS)}\n\n' + \
          msg_builder.settings_msg(session.settings)
    await session.ctx.send(msg)


async def send_edit_msg(session: Session):
    msg = 'Continuing pomodoro session with new settings!\n\n' + \
          msg_builder.settings_msg(session.settings)
    await session.ctx.send(msg)


async def send_countdown_msg(session: Session, title: str):
    countdown_msg = await session.ctx.send(f'**{title}**\n{session.timer.time_remaining_to_str()} left!')
    await countdown_msg.pin()
    session.countdown_msg = CountdownMsg(title, countdown_msg)
