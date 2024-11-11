#!/bin/bash

host=$(hostname | awk -F'.' '{print $1}')
timestamp=$(date +%Y_%m_%d)
now=$(date "+%Y-%m-%d %T")

#-----------
# This script is meant to be run by a cronjob
# set your bot/log directory or the cronjob won't find the files!

BOTDIR="/exp/icarus/app/users/mvicenzi/FNALBeamBot"
LOGFILE="/exp/icarus/data/users/mvicenzi/botlogs/attempt_bot_${host}_${timestamp}.log"

#-----------

if [[ ! -d ${BOTDIR}/env ]]; then
  echo "$now : Creating python environment in ${BOTDIR}" >> ${LOGFILE}
  python3 -m venv ${BOTDIR}/env
  source ${BOTDIR}/env/bin/activate
  python3 -m pip install --upgrade pip -q 2>&1
  pip install -r ${BOTDIR}/requirements.txt -q 2>&1
else
  echo "$now : Sourcing python environment..." >> ${LOGFILE}
  source ${BOTDIR}/env/bin/activate
fi

echo "$now : Attempting to run FNALBeamBot!" >> ${LOGFILE}
python3 ${BOTDIR}/runFNALBeamBot.py -l "INFO" >> ${LOGFILE} 2>&1

# clean-up old attempt logs
find $(dirname $LOGFILE)/attempt_* -type f -mtime +2 -exec rm -f {} \; >> ${LOGFILE} 2>&1

echo "$now : Execution completed!" >> ${LOGFILE}

exit 0
