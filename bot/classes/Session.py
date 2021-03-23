import discord
import state_handler
import msg_builder
import user_messages as u_msg
from Settings import Settings
from Timer import Timer
import random
import config
import asyncio
from asyncio import sleep
import player
import time as t


class Session:

    def __init__(self, settings: Settings, ctx):

        self.state = state_handler.POMODORO
        self.pomos_completed = 0
        self.settings = settings
        self.timer = Timer(self)
        self.ctx = ctx
        self.timeout = 0
        self.subscribers = set()

    @classmethod
    def is_connected_to_vc(cls, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @classmethod
    async def get_session(cls, ctx):
        return config.active_sessions.get(ctx.guild.id)

    async def send_start_msg(self, ctx):
        msg = f'{random.choice(u_msg.GREETINGS)}\n\n' + \
              msg_builder.settings_msg(self.settings)
        await ctx.send(msg)

    async def send_edit_msg(self, ctx):
        msg = 'Continuing pomodoro session with new settings!\n\n' + \
              msg_builder.settings_msg(self.settings)
        await ctx.send(msg)

    async def resume(self, ctx):
        self.timeout = t.time() + config.TIMEOUT
        timer_end = self.timer.end
        while True:
            await sleep(self.timer.remaining)
            session = await self.get_session(ctx)
            if not (session and
                    session.timer.running and
                    timer_end == session.timer.end):
                break
            else:
                await self.kill_if_idle()
                await player.alert(self)
                await state_handler.transition_session(self, ctx)

    async def start(self, ctx):
        config.active_sessions[ctx.guild.id] = self
        await self.send_start_msg(ctx)
        await player.alert(self)
        await self.resume(ctx)

    async def edit(self, ctx, duration, short_break, long_break, intervals):
        short_break = short_break or self.settings.short_break
        long_break = long_break or self.settings.long_break
        intervals = intervals or self.settings.intervals
        if not await Settings.is_valid(ctx, duration, short_break, long_break, intervals):
            return

        self.settings = Settings(duration, short_break, long_break, intervals)
        await self.send_edit_msg(ctx)

    async def kill_if_idle(self):
        ctx = self.ctx
        if not Session.is_connected_to_vc(ctx) \
                or len(ctx.voice_client.channel.members) < 2:
            await ctx.invoke(ctx.bot.get_command('stop'))
        if t.time() < self.timeout:
            return
        else:
            def check(reaction, user):
                return reaction.emoji == '👍' and user != ctx.bot.user

            msg = await ctx.channel.send('Are you still there?')
            await msg.add_reaction('👍')
            try:
                await ctx.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.invoke(ctx.bot.get_command('stop'))
            else:
                await ctx.send(random.choice(u_msg.STILL_THERE))
                if self.timer.running:
                    self.timeout = t.time() + config.TIMEOUT
                else:
                    self.timeout = t.time() + config.PAUSE_TIMEOUT
