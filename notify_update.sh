#!/bin/bash

# Load environment variables
source vars.sh

# Variables
TELEGRAM_BOT_TOKEN=$TOKEN
CHAT_ID=$ID_GROUP

# Get the latest commit message and escape special characters
commit_message=$(git log -1 --pretty=format:"%s")

# Format the message for Telegram with a code block and handle newlines
message="""
\`\`\`Bot Update Notification
$commit_message

The bot has been updated successfully.\`\`\`"""

# Create an inline keyboard with a button for suggestions or feedback
keyboard='{
  "inline_keyboard": [
    [{"text": "LEARN MORE", "url": "https://t.me/YourBot"}]
  ]
}'

# Send a notification to Telegram
curl -s -X POST https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage \
     -d chat_id=$CHAT_ID \
     -d text="$message" \
     -d parse_mode="MarkdownV2" \
     -d reply_markup="$keyboard"
