#!/bin/bash

# This script is meant to remove the cronjob that runs the bot

echo "FNALBeamBot process is run via a cronjob."
echo "Current user is $(whoami)."

COMMAND="$(PWD)/runFNALBeamBot.sh"

if crontab -l 2>&1 | grep -Fq $COMMAND; then
  
  old=$(crontab -l 2>/dev/null)
  new=$(echo "$old" | grep -v "$COMMAND")
  
  echo "$new" | crontab -
  echo "FNALBeamBot cronjob removed for $(whoami)!"
  crontab -l 

else
  
  echo "Cronjob does not exist for $(whoami)!"
  crontab -l  
  exit 0

fi

exit 0
