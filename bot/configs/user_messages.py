import config

NO_ACTIVE_SESSION_ERR = 'No active session.\n' \
                        f'Use command \'{config.CMD_PREFIX}start [pomodoro] [short_break] [long_break] [intervals]\'.'

ACTIVE_SESSION_EXISTS_ERR = 'There is already an active session on the server.\n'  # TODO multi-server upgrade ^
# TODO 'a session has already been started from this text channel'

ACTIVE_VOICE_CLIENT_EXISTS_ERR = 'Pomomo is already connected to this voice channel.'

NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR = f'Use durations between 1 and {config.MAX_INTERVAL_MINUTES} minutes.'

NUM_OUTSIDE_ONE_AND_SIXTY_ERR = 'Duration must be between 1 and 60 minutes.'

MISSING_ARG_ERR = 'Pass in at least one number.'

GREETINGS = ['Howdy howdy! Let\'s do this thang.',
             'Hey there! Let\'s get started!',
             'It\'s productivity o\'clock!',
             'Let\'s ketchup on some work!']

ENCOURAGEMENTS = ['Let\'s keep it going!',
                  'Keep up the good work!',
                  'That\'s what I\'m talking about!',
                  'You got this!',
                  'You\'re doing amazing!']

STILL_THERE = ['Phew...I was getting nervous 😅',
               'Gotcha! Just checking 😊',
               'Cool beans!']
