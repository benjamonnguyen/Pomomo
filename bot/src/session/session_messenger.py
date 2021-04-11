import random

from discord import Embed, Colour

from .Session import Session
from ..utils import msg_builder
from configs import user_messages as u_msg


async def send_start_msg(session: Session):
    await session.ctx.send(random.choice(u_msg.GREETINGS),
                           embed=msg_builder.settings_embed(session))


async def send_edit_msg(session: Session):
    await session.ctx.send('Continuing pomodoro session with new settings!',
                           embed=msg_builder.settings_embed(session))


async def send_countdown_msg(session: Session, title: str):
    title += '\u2800' * max((18 - len(title)), 0)
    embed = Embed(title=title, description=f'{session.timer.time_remaining_to_str()} left!', colour=Colour.green())
    session.bot_start_msg = await session.ctx.send(embed=embed)
    await session.bot_start_msg.pin()
