import commands
import random

NO_ACTIVE_SESSION = 'No active session.\n' \
                    'Use command \'pom!start [duration] [short_break] [long_break] [intervals]\'.'
ACTIVE_SESSION = 'There is an active pomodoro session.\nUse commands \'pom!stop\' or \'pom!resume\'.'
GREETINGS = ['Howdy y\'all! Let\'s do this thang!',
             'Nice to meet you! Let\'s get started!',
             'It\'s productivity o\'clock!']


def build_start_msg(duration, short_break, long_break, interval):
    msg = f'{random.choice(GREETINGS)}\n\n'\
          f'Duration: {duration} min\n'\
          f'Short break: {short_break} min\n'\
          f'Long break: {long_break} min\n'\
          f'Long break interval: {interval}'
    return msg


def build_edit_msg(duration, short_break, long_break, interval):
    msg = 'Starting pomodoro with new settings!\n\n'\
          f'Duration: {duration} min\n'\
          f'Short break: {short_break} min\n'\
          f'Long break: {long_break} min\n'\
          f'Long break interval: {interval}'
    return msg


def build_help_msg(for_command):
    msg = '```COMMANDS:\n\n'
    command_info = commands.INFO.values()
    if for_command == '':
        for command in command_info:
            msg += f'{command[0]}\n'
        msg += '\nFor more info on a specific command, type \'pom!help [command]\'```'
    else:
        if for_command in command_info:
            command = command_info(for_command)
            msg += command[0] + '\n' + command[1] + '```'
        else:
            msg = 'Enter a valid command.'
    return msg
