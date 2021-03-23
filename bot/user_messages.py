import config

NO_ACTIVE_SESSION = 'No active session.\n' \
                    f'Use command \'{config.CMD_PREFIX}start [pomodoro] [short_break] [long_break] [intervals]\'.'

ACTIVE_SESSION = 'There is already an active pomodoro session in your voice channel.\n'

GREETINGS = ['Howdy y\'all! Let\'s do this thang.',
             'Nice to meet you! Let\'s get started!',
             'It\'s productivity o\'clock!']

INV_NUM = 'Must use numbers greater than 0.'

JOIN_CHANNEL = 'Join a voice channel to use Pomomobot!'