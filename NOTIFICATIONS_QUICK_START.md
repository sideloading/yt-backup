# Notifications Quick Start

## Simple 3-Step Setup

### 1. Install Apprise (optional)
```bash
pip install apprise
```

### 2. Configure notifications in config.json
```json
{
  "notifications": {
    "enabled": true,
    "send_test_on_run": false,
    "apprise_urls": [
      "tgram://YOUR_BOT_TOKEN/YOUR_CHAT_ID"
    ],
    "events": {
      "channel_offline": true,
      "video_offline": true,
      "quota_exceeded": true
    }
  }
}
```

**Note:** Set `send_test_on_run: true` if you want a test notification every time you run `python3 yt-backup.py run`

### 3. Test it
```bash
python3 yt-backup.py test_notifications
```

## What You'll Get Notified About

- **channel_offline**: When a YouTube channel goes offline/deleted
- **video_offline**: When videos are removed or made private
- **quota_exceeded**: When YouTube API quota limit is hit

## Popular Services

**Telegram:**
```json
"apprise_urls": ["tgram://bot_token/chat_id"]
```

**Discord:**
```json
"apprise_urls": ["discord://webhook_id/webhook_token"]
```

**Email:**
```json
"apprise_urls": ["mailto://user:pass@gmail.com"]
```

**Multiple services:**
```json
"apprise_urls": [
  "tgram://bot_token/chat_id",
  "discord://webhook_id/webhook_token"
]
```

## That's It!

Run `python3 yt-backup.py run` and you'll get a test notification at startup, then real notifications as events occur.

No notifications section in config? No problem - script runs normally without it.
