import os
from dotenv import load_dotenv
from discord.ext import commands
import config

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix=config.CMD_PREFIX, help_command=None)

if __name__ == '__main__':
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded cogs.{filename[:-3]}\n')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
# TODO heroku
