# Pomomo
[![Discord Bots](https://top.gg/api/widget/status/821952460909445130.svg)](https://top.gg/bot/821952460909445130)
[![Discord Bots](https://top.gg/api/widget/servers/821952460909445130.svg?noavatar=true)](https://top.gg/bot/821952460909445130)

Pomodoro Discord Bot

<a href="https://discord.com/api/oauth2/authorize?client_id=821952460909445130&permissions=15739904&scope=bot">Invite Pomomo to your server!</a>
__________
NOTE: This source code only includes Pomomo's base features and is no longer up to date with the actual Pomomo bot. However, if you self-host a bot using this code, it would still be fully functional!

![Imgur Image](https://i.imgur.com/JzErsQC.png)<br><br>
Pomomo was inspired by a need to balance productivity and socializing. 
It uses the proven Pomodoro technique which alternates periods of work and relaxation 
to maximize productivity while minimizing burnout.

Designate time to focus so everyone can get stuff done while hanging out! You can customize the duration of any of the intervals to whatever works best for you.

### Features

* Play an alert in your voice channel whenever your pomodoro or break is over.

* Keep track of the session through the text channel the command was sent from or in your DMs if you're subscribed to the session.

* Set a countdown timer that updates in real time!

* Automatically mute/deafen during pomodoro intervals.

  * Preserves voice states so that members can't use Pomomo to undo a server mute/deafen from another source.

* Set reminder alerts to play before your intervals are about to end.

* Lock session so that only members with roles high enough can control the session.

* Help menu translations available: français, nederlands, español, 
italiano

### Demo

![Imgur Image](https://i.imgur.com/YOywEGi.png)

![Giphy Gif](https://media.giphy.com/media/rD2aQ1uPCetKN8zpI6/giphy.gif)

### Commands
#### Main Controls
>**start \[pomodoro] \[short_break] \[long_break] \[intervals]**\
>Start pomodoro session with optional custom settings (Default values are 20, 5, 15, 4)

>**pause**\
>Pause session

>**resume**\
>Resume session

>**restart**\
>Restart timer

>**skip**\
>Skip current interval and start the next pomodoro or break

>**end**\
>End session

>**edit \<pomodoro> \[short_break] \[long_break] \[interval]**\
>Continue session with new settings

#### More Controls

>**countdown \<duration> \[title]**\
>Start a countdown which sends a pinned message with a timer that updates in real time\
>You can also set a custom title (Default: "Countdown")

>**remind [focus_interval] [short_break] [long_break]**\
>Turn on early reminder alerts (Defaults: 5, 1, 5)\
>Pass in 0 if you do not want a reminder for the interval

>**remind_off**\
>Turn off reminder alerts

>**volume \<level>**\
>Change volume for alerts (Default: 5)

#### Info
>**status**\
>Get timer status

>**stats**\
>Get session stats

>**settings**\
>Get settings for session

#### Admin
>**lock [role]**\
>Lock control commands from being used by members with roles below the author's role or whatever server role is specified\
>This can be overridden by any member with a higher role

>**unlock**\
>Unlock restrictions on control commands for the session

#### Subscription
>**dm**\
>Toggle subscription to get DM alerts for the server's session

>**autoshush <me|all> \[mute_only]**\
>Toggle subscription to get automatically deafened and muted during pomodoro intervals.\
> Optionally add the \"mute_only\" parameter if you do not want to be deafened during focus intervals.
>Only members with mute and deafen permissions can use "all" to autoshush everyone in the pomodoro voice channel.

### Footnotes

Pomomo is pretty barebones but does what it does super well! 
I want to make sure the bot is simple, easy to use, and lightweight.

Drop by the support server [here](https://discord.gg/Aghy78wcFr) to leave a suggestion or report a bug.

If you'd like to make a donation, you can [buy me a coffee](https://www.buymeacoffee.com/benjamonn) or subscribe to [Pomomo Plus](https://pomomo.bot/premium)!

Attributions:
Sound effects obtained from <a href="https://www.zapsplat.com/">www.zapsplat.com</a>
