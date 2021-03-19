START_ARGS = 'duration: duration of each pomodoro in minutes\n'\
             'short_break: duration of short breaks in minutes\n'\
             'long_break: duration of long breaks in minutes\n'\
             'intervals: number of pomodoros between each long break'

INFO = {'start': ['start [duration] [short_break] [long_break] [intervals]',
                  'Start pomodoro session with optional custom settings\n\n' + START_ARGS],
        'pause': ['pause', 'Pause pomodoro session'],
        'resume': ['resume', 'Resume pomodoro session'],
        'time': ['time', 'Get time remaining'],
        'restart': ['restart', 'Restart timer'],
        'skip': ['skip', 'Skip current interval and start the next pomodoro or break'],
        'edit': ['edit duration [short_break] [long_break] [interval]',
                 'Continue pomodoro session with new settings\n\n' + START_ARGS],
        'stop': ['stop', 'End pomodoro session'],
        }
