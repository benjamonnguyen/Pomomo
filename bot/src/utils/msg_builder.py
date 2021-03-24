from configs import config, help_info
from Settings import Settings


def settings_msg(settings: Settings) -> str:
    return f'Pomodoro: {settings.duration} min\n' \
           f'Short break: {settings.short_break} min\n' \
           f'Long break: {settings.long_break} min\n' \
           f'Long break interval: {settings.intervals}'


def help_msg(for_command):
    msg = '```'
    command_info = help_info.CMD_INFO
    if for_command == '':
        msg += f'{help_info.SUMMARY}COMMANDS:\n'
        for command in command_info.values():
            msg += f'{command[0]}\n'
        msg += f'\nFor more info on a specific command, type \'{config.CMD_PREFIX}help [command]\'\n\n'\
               + help_info.CONTACT + '```'
    else:
        if for_command in command_info.keys():
            command = command_info.get(for_command)
            msg += command[0] + ' \n' + command[1] + '```'
        else:
            msg = 'Enter a valid command.'
    return msg
