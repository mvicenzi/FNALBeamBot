###############################
### Bot configuration parameters
###############################

# Connection to Channel 13
url = 'https://www-bd.fnal.gov/cgi-bin/notify_mes.pl?ch13=text'

# Connection to Slack workspace
slack_token = 'xoxb-xxxx-xxxx-xxxx'
slack_channels = ['#fnal-beam-news','#icarus-shift-operations']
message_template = 'botMessage.json'

# DB file 
db_file = 'notices.db'

# Logging
log_directory = './'
log_level = 'INFO'
