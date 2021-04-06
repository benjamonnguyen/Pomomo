import config


SUMMARY = 'Pomomo helps keep you and your friends on track while you study together!\n' \
          'Set periods of focus to get work done and chat during the breaks.\n\n' \
          'Required parameters are enclosed in <> and optional parameters are enclosed in []\n' \
          f'Example usage: {config.CMD_PREFIX}start 30 5 15\n'

POMO_ARGS = 'pomodoro: duration of each pomodoro in minutes (Default: 20 min)\n' \
            'short_break: duration of short breaks in minutes (Default: 5 min)\n' \
            'long_break: duration of long breaks in minutes (Default: 15 min)\n' \
            'intervals: number of pomodoros between each long break (Default: 4)'

COUNTDOWN_ARGS = 'Enclose title in " " if longer than one word (Default: \"Countdown\").\n' \
                 'You can optionally add the \"mute\" parameter to disable the voice channel audio alert.'

COMMANDS = {'Control commands': {'start': ['start [pomodoro] [short_break] [long_break] [intervals]',
                                           'Start pomodoro session with optional custom settings.\n\n' + POMO_ARGS],
                                 'pause': ['pause', 'Pause session'],
                                 'resume': ['resume', 'Resume session'],
                                 'restart': ['restart', 'Restart timer'],
                                 'skip': ['skip', 'Skip current interval and start the next pomodoro or break.'],
                                 'stop': ['stop', 'End session'],
                                 'edit': ['edit <duration> [short_break] [long_break] [interval]',
                                          'Continue session with new settings\n\n' + POMO_ARGS],
                                 'countdown': ['countdown <duration> [title] [mute]',
                                               'Start a countdown which sends a pinned message '
                                               'with a timer that updates in real time.\n\n' +
                                               COUNTDOWN_ARGS]
                                 },
            'Info commands': {'time': ['time', 'Get time remaining'],
                              'stats': ['stats', 'Get session stats'],
                              'settings': ['settings', 'Get session settings']},
            'Subscription commands': {'dm': ['dm', 'Toggle subscription to get DM alerts for the server\'s session.'],
                                      'autoshush': ['autoshush [all]', 'Toggle subscription to get automatically'
                                                                       ' deafened and muted during '
                                                                       'pomodoro intervals.\n'
                                                                       'Members with mute and deafen permissions '
                                                                       'can add the \"all\" parameter to auto_shush '
                                                                       'everyone in the pomodoro voice channel.']}}

LINKS = 'Invite Pomomo to your server [here]' \
        '(https://discord.com/api/oauth2/authorize?client_id=821952460909445130&permissions=3155968&scope=bot)!\n' \
        'If you have any suggestions or want to report a bug, visit the support server [here]' \
        '(https://discord.gg/whszbaXd) or check out the [top.gg](https://top.gg/bot/821952460909445130) ' \
        'page for more info.\n\n' \
        'You can also support Pomomo by buying me a coffee [here](https://www.buymeacoffee.com/benjamonn) :)'
