#!/bin/bash

echo "Remaining FNALBeamBot processes:"
ps aux | grep '[Pp]ython bot.py'

echo "Killing remaining FNALBeamBot processes..."
kill -9 $(ps aux | grep '[Pp]ython bot.py' | awk '{print $2}')

echo "Starting FNALBeamBot..."

source env/bin/activate
python bot.py -w 300 -l "INFO" &

echo "FNALBeamBot started."

