import config

NO_ACTIVE_SESSION = 'No active session.\n' \
                    f'Use command \'{config.CMD_PREFIX}start [pomodoro] [short_break] [long_break] [intervals]\'.'

ACTIVE_SESSION = 'There is already an active pomodoro session on the server.\n'

GREETINGS = ['Howdy howdy! Let\'s do this thang.',
             'Hey there! Let\'s get started!',
             'It\'s productivity o\'clock!']

INV_NUM = 'Must use numbers greater than 0.'

JOIN_CHANNEL = 'Join a voice channel to use Pomomobot!'

STILL_THERE = ['Phew...I was getting nervous 😅',
               'Gotcha! Just checking 😊',
               'Cool beans!']