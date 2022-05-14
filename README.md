
# yt-backup  
![version](https://img.shields.io/github/v/release/w0d4/yt-backup?color=0e7fc0&include_prereleases&style=flat-square)

Backup utility for YouTube, using yt-dlp/youtube-dl alongside Google's YouTube Data API v3. 

* Utilizes Google's YouTube API to fetch metadata of channels/playlists/videos to avoid rate limits
* Supports checking hundreds of channels per run (within API limits)
* Metadata such as filesize, video length, video descriptions stored in a SQL database, via SQLAlchemy
* Grafana Dashboards for visualisation of data, as well as live monitoring
* Proxy support


##  Dependencies
* [Python 3.x.](http://www.python.org/)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [Rclone](https://rclone.org/)
* A working SQL database with utf8mb4 support
* Google YouTube Data API v3, YouTube API key
* Grafana Dashboard (Optional)

## Installation
1. Clone this repo
2. Create a user in your DBMS with write permissions for a schema with utf8mb4 encoding
```sql
CREATE DATABASE mydatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL ON mydatabase.* TO 'user' IDENTIFIED BY 'password';
```
3. Configure an Rclone remote. If remote points to cloud storage, crypt remote strongly recommended. 
4. Modify `config.json.example` to match your system paths, database and Rclone remote. Save as `config.json`
5. Create your YouTube API client_secret.json file and place inside the project directory 
6. (Optional) Add your database as datasource in Grafana. Suggested name `yt-backup`.

### Creating client_secret.json file
- Go to the Google [console](https://console.developers.google.com/).
- *Create project*.
- Side menu: *APIs & auth -> APIs*.
- Top menu: *Enabled API(s)*: Enable all YouTube APIs.
- Side menu: *APIs & auth -> Credentials*.
- *Create a Client ID*: Add credentials -> OAuth 2.0 Client ID -> Other -> Name: youtube-download -> Create -> OK
- *Download JSON*: Under the section "OAuth 2.0 client IDs". Save the file to your local system.
- Copy this JSON to `client_secret.json` in the project directory.


### Automatic downloading using systemd
- Copy yt-backup.service and yt-backup.timer from systemd-units folder to /etc/systemd/system/
- Edit /etc/systemd/system/yt-backup.service and replace all placeholders with your system specific values
- Edit /etc/systemd/system/yt-backup.timer and insert as many times as you want
- As root run `systemctl daemon-reload`
- As root run `systemctl enable --now yt-backup.timer`

## Config options

| **Name**       |                       | **Example**                                                                          | **Description**                                                                                                                               |
|----------------|-----------------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| **database**   | connection_info       | "mysql+mysqldb://username:password@192.168.1.10:3306/ database_name?charset=utf8mb4" | Connection information to your database. Append ?charset=utf8mb4 to match DB.                                                                 |
| **base**       | download_dir          | "/mnt/shares/yt-backup/tmp"                                                          | Directory where yt-dlp will put your videos before uploading it to destination via Rclone. **WARNING** This directory is erased on each run.  |
|                | download_lockfile     | "/tmp/yt-backup-lockfile"                                                            | Location of lockfile, prevents any conflicts multiple runs at one time.                                                                       |
|                | channel_naming        | "%channel_name [%channel_id]"                                                        | Define channel name per yt-dlp's [output template]().                                                                                         |
|                | proxy_restart_command |                                                                                      | If you have a proxy which can change it's IP address, enter it's restart command here.                                                        |
| **rclone**     | binary_path           | "/usr/bin/rclone"                                                                    |                                                                                                                                               |
|                | config_path           | "/home/user/.config/rclone/rclone.conf"                                              | Rclone config path.                                                                                                                           |
|                | move_or_copy          | "move"                                                                               | move or copy videos after download. Strongly recommend _move_.                                                                                |
|                | upload_base_path      | "YouTube"                                                                            | Path where downloaded files will be uploaded to.                                                                                              |
|                | upload_target         | "b2"                                                                                 | The Rclone remote where the downloaded files will be uploaded to.                                                                             |
| **youtube-dl** | binary_path           | "/usr/local/bin/yt-dlp"                                                              | Location of yt-dlp binary.                                                                                                                    |
|                | download-archive      | "/mnt/shares/yt-backup/archive.list"                                                 | yt-dlp archive file                                                                                                                           |
|                | video-format          | "(bestvideo+bestaudio/best)"                                                         | Refer to yt-dlp's [format selection](). Defaults to best video possible.                                                                      |
|                | naming-format         | "%(upload_date)s %(title).100s %(height)sp  %(id)s.%(ext)s"                          | Custom naming format, refer to yt-dlp's [output template]().                                                                                  |
|                | additional-options    | --cookies /path/to/cookies.txt  --external-downloader aria2c                         | (optional) extra flags to be passed to yt-dlp for downloading.                                                                                |
|                | min_sleep_interval    | 5                                                                                    | How many seconds to sleep between each video downloads minimum                                                                                |
|                | max_sleep_interval    | 60                                                                                   | How many seconds to sleep between each video downloads maximum                                                                                |
|                | proxy                 | socks5://127.0.0.1:1080                                                              | (optional) specify proxy and port which yt-dlp should use. Leave empty for no proxy usage.                                                    |


## Usage
### Get help output
- `python3 yt-backup.py --help`

### Add a channel
#### By channel ID (better option)
- `python3 yt-backup.py add_channel --channel_id <youtube-channel-id>`
#### By channel ID with custom channel name
- `python3 yt-backup.py add_channel --channel_id <youtube-channel-id> --username <custom name>`
#### By username
- `python3 yt-backup.py add_channel --username <youtube-user-id>`
#### By channel id with downloading all playlists and video infos and limit video download to videos starting from now
- `python3 yt-backup.py add_channel --channel_id <youtube-channel-id> --all_meta --download_from now`

### Get all playlists for channels
#### For all channels
- `python3 yt-backup.py get_playlists`
#### For only one channel
- `python3 yt-backup.py get_playlists --channel_id <youtube channel_id>`

### Get all videos from all playlists
- `python3 yt-backup.py get_video_infos`

### Download all videos which are not downloaded currently
- `python3 yt-backup.py download_videos`

### Download all videos from one specific playlist ID
- `python3 yt-backup.py download_videos --playlist_id`

#### Force refresh playlist for new videos (or all)
- `python3 yt-backup.py get_video_infos --playlist_id <id> --force_refresh`

All videos which are in database, but not in the channel's playlist anymore, will be marked as offline.

If you want to know if they are completely gone or just private, you should run `python3 yt-backup.py verify_offline_videos`

### Generate Statistics
- `python3 yt-backup.py generate_statistics --statistics <archive_size,videos_monitored,videos_downloaded>`

### Get playlists, get video infos, download new videos, check all offline videos against youtube API and generate statistics in one command
- `python3 yt-backup.py run`

### Enable or disable the download for videos of a channel
- `python3 yt-backup.py toggle_channel_download --username <channel_name> --disable`
- `python3 yt-backup.py toggle_channel_download --username <channel_name> --enable`

### Verify all marked offline videos if they are really offline or only private
- `python3 yt-backup.py verify_offline_videos`
All videos which are marked as offline in database will be checked in packages of 50 videos against the YouTube API. Each video which is not returned in answer, will be marked as offline. If a video is part of the answer, it will be marked as online again or as unlisted if the API reports this.

### Verify all channels online status
- `python3 yt-backup.py verify_channels`
This will check all channel IDs against youtube API if they are still online. If not, they will be set offline. Also all playlists and videos of the channels.

### Reset YouTube API quota information
- `python3 yt-backup.py --reset_quota_exceeded_state`
Resets the quota exceeded state in case something gone wrong during calculation


### List channels with playlists
#### For all channels
- `python3 yt-backup.py list_playlists`
#### For only one channel by username
- `python3 yt-backup.py list_playlists --username <channel name from DB>`
#### For only one channel by channel ID
- `python3 yt-backup.py list_playlists --channel_id <channel_id>`

### Modify a playlist
#### Set a specific date and time for download date limit
- `python3 yt-backup.py modify_playlist --playlist_id <playlist_id> --download_from "2019-06-01 00:00:00"`
#### Remove download date limit from playlist
- `python3 yt-backup.py modify_playlist --playlist_id <playlist_id> --download_from all`
##### What will happen?
If a video has no upload date, it will be checked against YouTube API to get download date.
If a videos upload date is newer than it's playlist download date limit, download required will be set to 1. Else it will be set to 0.
#### Change a playlists monitored state
- `python3 yt-backup.py modify_playlist --playlist_id <playlist_id> --monitored <0/1>`

### Rename a channel
- `python3 yt-backup.py modify_channel --channel_id <channel_id> --username <new channel name>`
The channel will be renamed in database to something new. Spaces will be replaced by _.
No files will be moved. You have to do this by hand.

### Add a playlist manually
You can add a playlist by hand. This can be useful in case you have the playlist ID of a unlisted Playlist
For this you need the playlist ID and the channel ID to which the playlist belongs
Optionally you can add --playlist_name <name> and --monitored <1/0> in case you want to change the defaults
- `python3 yt-backup.py add_playlist --playlist_id <playlist_id> --channel_id <channel_id>`

### Add a single video
You can add a single video to the script. You must specify the video_id with --video_id
If the video belongs to a channel which is not in database, it will be added
If the channel must be added, it's playlists will be fetched and added as not monitored, so only the added video will be in the playlist

Optionally, you can add the following parameters (all values are sample values):
- --downloaded "YYYY-MM-DD hh:mm:ss" in case you have the video already downloaded
- --resolution 1920x1080
- --size 12345 (size must be specified in bytes)
- --duration 1234s (duration must be specified in seconds)
- --video_status unlisted (default is online, if you want to add an unlisted video, use unlisted)
- `python3 yt-backup.py add_video --video_id <video_id>`


## Grafana Dashboards
You need a running grafana installation for this.
There is also an [official docker](https://grafana.com/docs/grafana/latest/installation/docker/) image in case you do not have a running grafana installation.

### Create new views in your database
#### MySQL/MariaDB
```SQL
CREATE OR REPLACE
ALGORITHM = UNDEFINED
VIEW downloaded_and_available_videos_by_channel
AS SELECT 
t1.channel_name, video_count, COALESCE(downloaded_count,0) as downloaded_count
FROM (
	SELECT channels.channel_name AS channel_name,COUNT(*) AS video_count
	FROM videos
	INNER JOIN playlists ON videos.playlist=playlists.id
	INNER JOIN channels ON playlists.channel_id=channels.id GROUP BY playlists.id ORDER BY video_count DESC) t1
	LEFT JOIN (
		SELECT channels.channel_name AS channel_name,COUNT(*) AS downloaded_count
		FROM videos
		INNER JOIN playlists ON videos.playlist=playlists.id
		INNER JOIN channels ON playlists.channel_id=channels.id
		WHERE videos.downloaded IS NOT NULL
		GROUP BY playlists.id ORDER BY downloaded_count DESC) t2
	ON t1.channel_name = t2.channel_name
ORDER BY video_count DESC
```
```SQL
CREATE OR REPLACE
ALGORITHM=UNDEFINED 
VIEW downloaded_and_available_videos_by_channel_with_percent AS
select downloaded_and_available_videos_by_channel.channel_name AS channel_name,downloaded_and_available_videos_by_channel.video_count AS video_count,downloaded_and_available_videos_by_channel.downloaded_count AS downloaded_count,round(downloaded_and_available_videos_by_channel.downloaded_count * 100.0 / downloaded_and_available_videos_by_channel.video_count,1) AS Percent
FROM downloaded_and_available_videos_by_channel
```
```SQL
CREATE OR REPLACE
ALGORITHM=UNDEFINED
VIEW `videos_downloaded_at_date` AS
SELECT count(0) AS `number`,cast(`videos`.`downloaded` as date) AS `download_date`
FROM `videos` where `videos`.`downloaded` IS NOT NULL
GROUP BY cast(`videos`.`downloaded` as date)
```
```SQL
CREATE OR REPLACE
ALGORITHM=UNDEFINED
VIEW `size_downloaded_at_date` AS
SELECT SUM(size)/power(1024,3) AS `size`,cast(`videos`.`downloaded` as date) AS `download_date`
FROM `videos` where `videos`.`downloaded` IS NOT NULL
GROUP BY cast(`videos`.`downloaded` as date)
```

### Import the dashboard json files from [the grafana dashboards folder](https://github.com/w0d4/yt-backup/tree/master/grafana-dashboards) into your grafana installation
- https://grafana.com/docs/grafana/latest/reference/export_import/#importing-a-dashboard
- Correct all the links on the overview dashboard to match your dashboard IDs


## Problems
### I get strange error messages during run or get_video_infos regarding encoding errors
Make sure your database, tables and columns are created with utf8mb4 encoding support.

Execute the following statements against your database in case you are using MariaDB/MySQL. Make sure the only output is utf8mb4
```SQL
SELECT default_character_set_name FROM information_schema.SCHEMATA 
WHERE schema_name = "yt-backup";
```
```SQL
SELECT CCSA.character_set_name FROM information_schema.`TABLES` T,
       information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
WHERE CCSA.collation_name = T.table_collation
  AND T.table_schema = "yt-backup"
  AND T.table_name = "videos";
```
```SQL
SELECT character_set_name FROM information_schema.`COLUMNS` 
WHERE table_schema = "yt-backup"
  AND table_name = "videos"
  AND column_name = "description";
```

## License
Copyright (C) 2020  w0d4
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Questions
### What happens if a video is already marked as downloaded in youtube-dl archive, but not in database and download is started
yt-backup will find the video id in youtube-dl download archive and set it's download date to 1972-01-01 23:23:23 in database. Since we don't know when the video was downloaded originally, we have marked it as downloaded anyways.
