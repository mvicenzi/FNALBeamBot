#!/bin/bash

# This script is meant to be run by a cronjob
# If it find no active bot, it restarts it

# set your bot directory or the cronjob won't find the files!
botdir="/exp/icarus/app/users/mvicenzi/FNALBeamBot"

# get process id of bot if it exists
timestamp=`date +%Y_%m_%d_%H_%M`
pid=$(ps aux | grep '[Pp]ython bot.py' | awk '{print $2}')

if [[ -z "$pid" ]]; then

   echo "${timestamp}: no FNALBeamBot process found, restarting!"
   cd ${botdir}
   source env/bin/activate
   python bot.py -w 300 -l "INFO" &

fi
