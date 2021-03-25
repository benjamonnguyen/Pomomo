import config

NO_ACTIVE_SESSION_ERR = 'No active session.\n' \
                    f'Use command \'{config.CMD_PREFIX}start [pomodoro] [short_break] [long_break] [intervals]\'.'

ACTIVE_SESSION_EXISTS_ERR = 'There is already an active pomodoro session on the server.\n'

NUM_LT_ONE_ERR = 'Must use numbers greater than 0.'

GREETINGS = ['Howdy howdy! Let\'s do this thang.',
             'Hey there! Let\'s get started!',
             'It\'s productivity o\'clock!']

ENCOURAGEMENTS = ['Let\'s keep it going!',
                  'Keep up the good work!',
                  'That\'s some good stuff!']

STILL_THERE = ['Phew...I was getting nervous 😅',
               'Gotcha! Just checking 😊',
               'Cool beans!']
