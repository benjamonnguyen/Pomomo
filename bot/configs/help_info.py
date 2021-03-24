SUMMARY = 'Pomomo helps keep you and your friends on track while you study together!\n' \
          'Set periods of focus to get work done and chat during the breaks.\n\n'

START_ARGS = 'pomodoro: duration of each pomodoro in minutes\n' \
             'short_break: pomodoro of short breaks in minutes\n' \
             'long_break: pomodoro of long breaks in minutes\n' \
             'intervals: number of pomodoros between each long break'

CMD_INFO = {'start': ['start [pomodoro] [short_break] [long_break] [intervals]',
                      'Start pomodoro session2 with optional custom settings\n\n' + START_ARGS],
            'pause': ['pause', 'Pause session2'],
            'resume': ['resume', 'Resume session2'],
            'time': ['time', 'Get time remaining'],
            'dm': ['dm', 'Toggle subscription to get DM alerts for the server\'s session2'],
            'restart': ['restart', 'Restart timer'],
            'skip': ['skip', 'Skip current interval and start the next pomodoro or break'],
            'edit': ['edit <duration> [short_break] [long_break] [interval]',
                     'Continue session2 with new settings\n\n' + START_ARGS],
            'stop': ['stop', 'End session2']
            }

CONTACT = 'Send me an email at feedback.sum@gmail.com if you want to report a bug or make a suggestion!'
