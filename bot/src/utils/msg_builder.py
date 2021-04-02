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
        for cmds_key, cmds_dict in help_info.COMMANDS.items():
            values = ''
            for value in cmds_dict.values():
                values += f'{value[0]}\n'
            embed.add_field(name=cmds_key, value=values, inline=False)
        more_info = f'\nFor more info on a specific command, type \'{config.CMD_PREFIX}help [command]\'\n\n' \
                    + help_info.LINKS + help_info.CONTACT
        embed.add_field(name='\u200b', value=more_info, inline=False)
    else:
        for cmds_key, cmds_dict in help_info.COMMANDS.items():
            cmd_info = cmds_dict.get(for_command)
            if cmd_info:
                break
        if cmd_info:
            embed = Embed(title=cmd_info[0], description=cmd_info[1], colour=Colour.blue())
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
