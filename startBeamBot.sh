#!/bin/bash

# ---------------------------------------
# This script is meant to setup the cronjob that runs the bot
# Choose the interval in minutes (e.g. every 5 minutes)

INTERVAL=5

# ---------------------------------------

echo "FNALBeamBot process is run via a cronjob."
echo "Current user is $(whoami)."

COMMAND="${PWD}/runFNALBeamBot.sh"
CRON="*/$INTERVAL * * * * $COMMAND"

if crontab -l 2>&1 | grep -Fq $COMMAND; then

  echo "Cronjob already exists for $(whoami)!"
  crontab -l  
  exit 0

else
  
  echo "Setting up cronjob to run every $INTERVAL minutes."
  old=$(crontab -l 2>/dev/null)

  if [ -n "$old" ]; then
    new="${old}"$'\n'"${CRON}"
  else
    new="${CRON}"
  fi

  echo "$new" | crontab -
  echo "FNALBeamBot cronjob installed for $(whoami)!"
  crontab -l

fi

exit 0
