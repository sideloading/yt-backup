#!/bin/bash

#######
## Gets video info for a channel ##
#######

# If a video ID was passed as an argument, use it. Otherwise, prompt the user.
if [ -n "$1" ]; then
    videoID="$1"
else
    read -p "Enter videoID [ENTER]: " videoID
fi

mysql --user=grafanaReader --password=password -h 192.168.1.200 archive << EOF
SELECT vid.id, vid.playlist, vid.title, chan.channel_name, vid.downloaded, vid.resolution
FROM videos vid
INNER JOIN channels chan ON vid.playlist = chan.id
WHERE video_id = "$videoID" \G;
EOF
