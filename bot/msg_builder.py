import help_doc
import random
import config
import user_messages as u_msg


def start_msg(duration, short_break, long_break, interval):
    msg = f'{random.choice(u_msg.GREETINGS)}\n\n'\
          f'Duration: {duration} min\n'\
          f'Short break: {short_break} min\n'\
          f'Long break: {long_break} min\n'\
          f'Long break interval: {interval}'
    return msg


def edit_msg(duration, short_break, long_break, interval):
    msg = 'Starting pomodoro with new settings!\n\n'\
          f'Duration: {duration} min\n'\
          f'Short break: {short_break} min\n'\
          f'Long break: {long_break} min\n'\
          f'Long break interval: {interval}'
    return msg


def help_msg(for_command):
    msg = f'```{help_doc.SUMMARY}'
    command_info = help_doc.CMD_INFO
    if for_command == '':
        msg += 'COMMANDS:\n\n'
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
