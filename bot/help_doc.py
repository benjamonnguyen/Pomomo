SUMMARY = 'Pomomo helps keep you and your friends on track while you study together!\n' \
          'Set periods of productivity and chat during the breaks.\n\n'

START_ARGS = 'pomodoro: pomodoro of each pomodoro in minutes\n' \
             'short_break: pomodoro of short breaks in minutes\n' \
             'long_break: pomodoro of long breaks in minutes\n' \
             'intervals: number of pomodoros between each long break'

CMD_INFO = {'start': ['start [pomodoro] [short_break] [long_break] [intervals]',
                      'Start pomodoro session with optional custom settings\n\n' + START_ARGS],
            'pause': ['pause', 'Pause pomodoro session'],
            'resume': ['resume', 'Resume pomodoro session'],
            'time': ['time', 'Get time remaining'],
            'restart': ['restart', 'Restart timer'],
            'skip': ['skip', 'Skip current interval and start the next pomodoro or break'],
            'edit': ['edit <pomodoro> [short_break] [long_break] [interval]',
                     'Continue pomodoro session with new settings\n\n' + START_ARGS],
            'stop': ['stop', 'End pomodoro session']
            }

CONTACT = 'Send me an email at feedback.sum@gmail.com if you want to report a bug or make a suggestion!'
