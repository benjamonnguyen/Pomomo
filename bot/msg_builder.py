import help_doc
import config
import user_messages as u_msg
import Settings


def settings_msg(settings: Settings) -> str:
    return f'Pomodoro: {settings.duration} min\n' \
           f'Short break: {settings.short_break} min\n' \
           f'Long break: {settings.long_break} min\n' \
           f'Long break interval: {settings.intervals}'


def edit_msg(pomodoro, short_break, long_break, interval):
    msg = 'Continuing pomodoro session with new settings!\n\n' +\
          settings_msg(pomodoro, short_break, long_break, interval)
    return msg


def help_msg(for_command):
    msg = f'```{help_doc.SUMMARY}'
    command_info = help_doc.CMD_INFO
    if for_command == '':
        msg += 'COMMANDS:\n'
        for command in command_info.values():
            msg += f'{command[0]}\n'
        msg += f'\nFor more info on a specific command, type \'{config.CMD_PREFIX}help [command]\'\n\n'\
               + help_doc.CONTACT + '```'
    else:
        if for_command in command_info.keys():
            command = command_info.get(for_command)
            msg += command[0] + '\n\n' + command[1] + '```'
        else:
            msg = 'Enter a valid command.'
    return msg
