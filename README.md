# FNALBeamBot

**FNALBeamBot** is a bot that allows to display _Channel 13_ beam notifications from the **Fermilab Accelerator Complex** in a _Slack_ channel.
The bot monitors Channel 13 for updates with a tunable frequency, and reports any new messages to the specified channel.

Please note that access to the Channel 13 text notifications is available only within the Fermilab network.

## Running the bot
The bot is run under a user cronjob every few minutes.
Two bash scripts are provided to start (`startBeamBot.sh`) and stop (`stopBeamBot.sh`) the bot.
The former installs a new line in the user `crontab` to execute the bot every few minutes.
The latter removes the installed line thus stopping the execution of the bot.

The cronjob runs the `runFNALBeamBot.sh` script.
This script automatically creates a Python virtual environment with `requirements.txt`.
No other action is needed by the user apart from tuning the configuration.

## Configuration
The primary bot configuration can be changed in `scripts/config.py`:
```
# Connection to Channel13
url = 'https://www-bd.fnal.gov/cgi-bin/notify_mes.pl?ch13=text'

# Connection to Slack workspace
slack_token = 'xoxb-xxxx-xxxx-xxxx'
slack_channel = '#fnal-beam-news'
message_template = 'botMessage.json'

# DB file 
db_file = 'notices.db'

# Logging
log_directory = './'
log_level = 'INFO'
```

### Cronjob
The interval at which the cronjob runs is set in `startBeamBot.sh`.
The default is every 5 minutes:
```
# This script is meant to setup the cronjob that runs the bot
# Choose the interval in minutes (e.g. every 5 minutes)

INTERVAL=5
```

The cronjob script `runFNALBeamBot.sh` also needs to point to the main bot directory (top level of this repository).
In addition, a path for its logfile needs to be provided.
This logfile is useful to debug issues with the cronjob not running.
```
# This script is meant to be run by a cronjob
# set your bot/log directory or the cronjob won't find the files!

BOTDIR="/path/to/main/dir/FNALBeamBot"
LOGFILE="/path/to/cronjob/log/attempt_bot_${host}_${timestamp}.log"

```

### Slack message
Similarly, the `json` payload for the Slack message can be customized in `botMessage.json`.
The two keywords `%%date%%` and `%%message%%` are replaced by the bot with the actual contents of the notification.
```
{
  "blocks": [
		{
			"type": "divider"
		},
		{       "type": "section",
                        "text": 
			{
				"type": "mrkdwn",
				"text": ":fermilab: *Channel 13 Notification* on *%%date%%*\n>%%message%%\n>_For more information, check <https://www-bd.fnal.gov/Elog|AD Elog>_."
			}
		},
        	{	"type": "divider"
		}
	    ]
}

```
