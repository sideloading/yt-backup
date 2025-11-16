#!/bin/bash

run_count=0

while true
do
    # Increment the counter
    ((run_count++))
    # Get the current date and time
    current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
    # Remove any potential conflicts
    rm -f /tmp/yt-backup-lockfiles
    rm -f /tmp/yt-backup.log
    # Execute yt-backup
    python yt-backup.py run --ignore_429_lock #--debug
    #
    echo -e "\n\n$current_datetime - Retrying in 1-2 hours - Run count: $run_count\n\n"
    sleep "$(( $RANDOM % 3600 + 1800 ))"
done
