#!/bin/bash

run_count=0

while true
do
    # Increment the counter
    ((run_count++))
    # Get the current date and time
    current_datetime=$(date +"%Y-%m-%d %H:%M:%S")
    # Execute yt-backup
    python yt-backup.py verify_offline_videos &&
    python yt-backup.py generate_statistics --statistics archive_size,videos_monitored,videos_downloaded
    echo -e "\n\n$current_datetime - Retrying in 1-2 hours - Run count: $run_count\n\n"
    # sleep 8 hours
    sleep 28800
done
