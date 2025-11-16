#!/bin/bash

read -p "Enter watchID [ENTER]: " watchID

python yt-backup.py add_video --video_id="$watchID"

#echo "video added to the queue, run"
#echo "python3 yt-backup.py download_videos"
#echo "to begin downloading immediately"
#python3 yt-backup.py download_videos
