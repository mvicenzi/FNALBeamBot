###############################
### Bot configuration parameters
###############################

# Connection to Channel 13
url = 'https://www-bd.fnal.gov/cgi-bin/notify_mes.pl?ch13=text'

# Connection to Slack workspace
slack_token = 'xoxb-xxxx-xxxx-xxxx'
slack_channels = ['#fnal-beam-news','#icarus-shift-operations']
message_template = '/path/to/botMessage.json'

# DB file 
db_file = '/path/to/notices.db'

# Logging
log_directory = '/path/to/log/dir/'
log_level = 'INFO'
