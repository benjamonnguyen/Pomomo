import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from configs import config
from session import session_manager


intents = discord.Intents.default()
intents.typing = False
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=config.CMD_PREFIX, help_command=None, intents=intents)

if __name__ == '__main__':
    for filename in os.listdir(config.COGS_PATH):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    kill_idle_sessions.start()


@tasks.loop(minutes=30)
async def kill_idle_sessions():
    for session in session_manager.active_sessions.values():
        await session_manager.kill_if_idle(session)


bot.run(TOKEN)
