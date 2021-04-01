from bot.configs import config, help_info
from Settings import Settings
from Stats import Stats
from discord import Embed, Colour


def settings_embed(settings: Settings) -> Embed:
    settings = f'Pomodoro: {settings.duration} min\n' \
               f'Short break: {settings.short_break} min\n' \
               f'Long break: {settings.long_break} min\n' \
               f'Long break interval: {settings.intervals}'
    return Embed(title='Session settings', description=settings, colour=Colour.orange())


def help_embed(for_command):
    if for_command == '':
        embed = Embed(title='Help menu', description=help_info.SUMMARY, colour=Colour.blue())
        control_cmds = ''
        for command in help_info.CONTROL_CMDS.values():
            control_cmds += f'{command[0]}\n'
        embed.add_field(name='Control commands', value=control_cmds, inline=False)
        info_cmds = ''
        for command in help_info.INFO_CMDS.values():
            info_cmds += f'{command[0]}\n'
        embed.add_field(name='Info commands', value=info_cmds, inline=False)
        more_info = f'\nFor more info on a specific command, type \'{config.CMD_PREFIX}help [command]\'\n\n' \
                    + help_info.LINKS + help_info.CONTACT
        embed.add_field(name='\u200b', value=more_info, inline=False)
    else:
        command = help_info.CONTROL_CMDS.get(for_command) or help_info.INFO_CMDS.get(for_command)
        if command:
            embed = Embed(title=command[0], description=command[1], colour=Colour.blue())
        else:
            return
    return embed


def stats_msg(stats: Stats):
    pomo_str = 'pomodoros'
    minutes_str = 'minutes'
    if stats.pomos_completed == 1:
        pomo_str = 'pomodoro'
    if stats.minutes_completed == 1:
        minutes_str = 'minute'
    return f'{stats.pomos_completed} {pomo_str} ({stats.minutes_completed} {minutes_str})'
