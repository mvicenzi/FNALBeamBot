# FNALBeamBot

*FNALBeamBot* is a bot that allows to display _Channel 13_ beam notifications from the *Fermilab Accelerator Complex* in a _Slack_ channel.
The bot monitors Channel 13 for updates with a tunable frequency, and reports any new messages to the specified channel.

## Setup
Setup a Python virtual environment with `requirements.txt`:
```
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

## Configuration
The bot configuration can be changed in `scripts/config.py`:
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
```
### Slack message
Similarly, the `json` payload for the Slack message can be costumized in `botMessage.json`.
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

## Running the bot
Two bash scripts are provided to start (`runBeamBot.sh`) and stop (`stopBeamBot.sh`) the bot as a background process.
The bot can be started by running:
```
python bot.py --wait 300 --logging [True/False]
```
