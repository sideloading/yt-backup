#!/bin/bash

#######
## Removes and re-adds 360p video ##
#######

# If a video ID was passed as an argument, use it. Otherwise, prompt the user.
if [ -n "$1" ]; then
    videoID="$1"
else
    read -p "Enter videoID [ENTER]: " videoID
fi

# Remove videoID from ytdl archive file (actually this appends it — adjust if truly removing)
echo "backing up archive.list"
cp archive.list archive.list.backup

echo "adding vid to archive.list..."
echo "youtube $videoID" >> archive.list

echo "done"
