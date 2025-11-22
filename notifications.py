# yt-backup command line utility to backup youtube channels easily
# Copyright (C) 2020  w0d4
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

logger = logging.getLogger('yt-backup')

# Try to import apprise, but don't fail if it's not installed
try:
    import apprise
    APPRISE_AVAILABLE = True
except ImportError:
    APPRISE_AVAILABLE = False
    logger.warning("Apprise library not installed. Notifications will be disabled. Install with: pip install apprise")


def _send_notification(config, title, body):
    """
    Internal helper to send notifications via Apprise.
    
    Args:
        config: Configuration dictionary containing notification settings
        title: Notification title
        body: Notification body text
    """
    if not APPRISE_AVAILABLE:
        logger.debug("Apprise not available, skipping notification")
        return
    
    notification_config = config.get("notifications", {})
    apprise_urls = notification_config.get("apprise_urls", [])
    
    if not apprise_urls:
        logger.debug("No apprise_urls configured, skipping notification")
        return
    
    apobj = apprise.Apprise()
    for url in apprise_urls:
        apobj.add(url)
    
    try:
        apobj.notify(body=body, title=title)
        logger.debug(f"Notification sent: {title}")
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")


def _is_notification_enabled(config, event_type):
    """
    Check if notifications are enabled globally and for a specific event type.
    
    Args:
        config: Configuration dictionary
        event_type: Type of event (e.g., 'channel_offline', 'video_offline')
    
    Returns:
        bool: True if notifications should be sent for this event
    """
    if "notifications" not in config:
        return False
    
    notification_config = config["notifications"]
    
    # Check global enabled flag
    if not notification_config.get("enabled", False):
        return False
    
    # Check event-specific flag
    events = notification_config.get("events", {})
    return events.get(event_type, False)


def send_channel_offline_notification(config, channel_name, channel_id):
    """
    Send a notification when a channel is marked offline.
    
    Args:
        config: Configuration dictionary containing notification settings
        channel_name: Name of the channel that went offline
        channel_id: YouTube channel ID
    """
    if not _is_notification_enabled(config, "channel_offline"):
        return
    
    channel_url = f"https://youtube.com/channel/{channel_id}"
    title = "YouTube Channel Offline"
    body = f"Channel '{channel_name}' has been marked offline.\n\nChannel URL: {channel_url}"
    
    _send_notification(config, title, body)
    logger.info(f"Sent offline notification for channel: {channel_name}")


def send_video_offline_notification(config, video_title, video_id, channel_name):
    """
    Send a notification when a video is marked offline.
    
    Args:
        config: Configuration dictionary
        video_title: Title of the video
        video_id: YouTube video ID
        channel_name: Name of the channel the video belongs to
    """
    if not _is_notification_enabled(config, "video_offline"):
        return
    
    video_url = f"https://youtube.com/watch?v={video_id}"
    title = "YouTube Video Offline"
    body = f"Video '{video_title}' from channel '{channel_name}' has been marked offline.\n\nVideo URL: {video_url}"
    
    _send_notification(config, title, body)
    logger.info(f"Sent offline notification for video: {video_title}")


def send_download_complete_notification(config, videos_downloaded, total_size_mb, duration_minutes):
    """
    Send a notification when a download run completes.
    
    Args:
        config: Configuration dictionary
        videos_downloaded: Number of videos downloaded
        total_size_mb: Total size downloaded in MB
        duration_minutes: Duration of download run in minutes
    """
    if not _is_notification_enabled(config, "download_complete"):
        return
    
    title = "Download Run Complete"
    body = f"Downloaded {videos_downloaded} video(s)\nTotal size: {total_size_mb:.2f} MB\nDuration: {duration_minutes:.1f} minutes"
    
    _send_notification(config, title, body)
    logger.info("Sent download complete notification")


def send_download_error_notification(config, error_type, video_title, video_id):
    """
    Send a notification when a download error occurs.
    
    Args:
        config: Configuration dictionary
        error_type: Type of error (e.g., 'HTTP 403', 'HTTP 429')
        video_title: Title of the video
        video_id: YouTube video ID
    """
    if not _is_notification_enabled(config, "download_errors"):
        return
    
    video_url = f"https://youtube.com/watch?v={video_id}"
    title = f"Download Error: {error_type}"
    body = f"Failed to download video '{video_title}'\nError: {error_type}\n\nVideo URL: {video_url}"
    
    _send_notification(config, title, body)
    logger.info(f"Sent download error notification for video: {video_title}")


def send_quota_exceeded_notification(config):
    """
    Send a notification when YouTube API quota is exceeded.
    
    Args:
        config: Configuration dictionary
    """
    if not _is_notification_enabled(config, "quota_exceeded"):
        return
    
    title = "YouTube API Quota Exceeded"
    body = "The YouTube API quota has been exceeded. Operations will resume automatically after the quota resets (typically within 24 hours)."
    
    _send_notification(config, title, body)
    logger.info("Sent quota exceeded notification")


def send_new_videos_notification(config, channel_name, video_count):
    """
    Send a notification when new videos are detected in a channel.
    
    Args:
        config: Configuration dictionary
        channel_name: Name of the channel
        video_count: Number of new videos detected
    """
    if not _is_notification_enabled(config, "new_videos"):
        return
    
    title = "New Videos Detected"
    body = f"Found {video_count} new video(s) in channel '{channel_name}'"
    
    _send_notification(config, title, body)
    logger.info(f"Sent new videos notification for channel: {channel_name}")
