import config

NO_ACTIVE_SESSION = 'No active session.\n' \
                    f'Use command \'{config.CMD_PREFIX}start [duration] [short_break] [long_break] [intervals]\'.'
ACTIVE_SESSION = 'There is an active pomodoro session.\n' \
                 f'Use commands \'{config.CMD_PREFIX}stop\' or \'{config.CMD_PREFIX}resume\'.'
GREETINGS = ['Howdy y\'all! Let\'s do this thang!',
             'Nice to meet you! Let\'s get started!',
             'It\'s productivity o\'clock!']

INV_NUM = 'Must use numbers greater than 0.'
