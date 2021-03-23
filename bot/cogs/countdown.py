from discord.ext import commands
import time as t
import user_messages as u_msg
import state
import config
import Timer


timer = Timer.Timer()


class Countdown(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def countdown(self, ctx, duration: int, pinned: True):
        if duration < 1:


    @countdown.error
    async def handle_error(self, ctx, error):
        error_msg = 'Pass in countdown duration greater than 0.'
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error_msg)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error_msg)
        else:
            print(error)

# TODO countdown(duration:int, pinned:bool)
# TODO check if user is still there
# TODO look into sharding
