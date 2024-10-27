import re
import hashlib
import asyncio
import logging
import time
import telegram
from langdetect import detect, LangDetectException 
from telegram.error import Forbidden
from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from collections import defaultdict
from better_profanity import profanity
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logging_utils import log_action, send_error_to_admin
from config import CHECK_INTERVAL, recent_messages, ID_GROUP, ID_ADMIN

profanity.load_censor_words()
warning_messages = defaultdict(list)
recent_urls = defaultdict(list)
toggle_message_content = {"toggle": True}
temporary_notified_users = set()
notified_users = set()
message_count = 0
authorized_words = {
'Word exeption allow'
}

def reset_temporary_notified_users():
    """Resets the list of temporarily notified users."""
    global temporary_notified_users
    temporary_notified_users.clear()
    log_action("temporary_notified_users has been reset.")

def reset_notified_users():
    """Resets the list of notified users."""
    global notified_users
    log_action(f"Notified users before reset: {len(notified_users)}")
    notified_users.clear()
    log_action("Notified users list reset.")

async def delete_warning_message(context, chat_id: int, message_id: int) -> None:
    """Deletes a warning message after a specified delay."""
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        log_action(f"Warning message {message_id} deleted in chat {chat_id}.")
    except Exception as e:
        logging.error(f"Error deleting warning message {message_id}: {e}")

def reset_old_hashes():
    """Purges old message hashes from recent_messages based on CHECK_INTERVAL."""
    current_time = time.time()
    for chat_id, messages in list(recent_messages.items()):
        recent_messages[chat_id] = [
            (image_hash, timestamp)
            for (image_hash, timestamp) in messages
            if (current_time - timestamp) < CHECK_INTERVAL
        ]
        if not recent_messages[chat_id]:
            del recent_messages[chat_id]
    log_action(f"Old hashes purged from recent_messages. Remaining chats: {len(recent_messages)}")

def schedule_daily_rules(application):
    """Schedules daily tasks like sending rules and resetting user lists."""
    scheduler = AsyncIOScheduler()
    logging.info("Scheduling daily jobs for rules and resetting notified users.")
    scheduler.add_job(send_group_rules, 'cron', hour=23, minute=30, args=[application]) 
    scheduler.add_job(reset_notified_users, 'cron', hour=23, minute=31)
    scheduler.add_job(reset_old_hashes, 'cron', hour=23, minute=32)
    scheduler.add_job(reset_temporary_notified_users, 'interval', seconds=60)
    scheduler.start()
    log_action("Daily jobs scheduled.")

async def get_image_hash(photo):
    """Computes the hash of an image."""
    logging.info(f"Fetching file for photo {photo.file_id}")
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()
    image_hash = hashlib.md5(file_bytes).hexdigest()
    logging.info(f"Generated hash for photo {photo.file_id}: {image_hash}")
    return image_hash

async def notify_user_once(context, chat_id, username, username_id, reason="duplicate"):
    """Notifies a user only once with a specific reason."""
    try:
        if username_id not in temporary_notified_users:
            notification_message_text = {
                "duplicate": f"Your message was deleted because it was a duplicate. Please avoid spamming.",
                "unauthorized_language": f"Your message was deleted due to language restrictions. Only English are allowed.",
                "inappropriate_language": f"Your message contained inappropriate language and was deleted. Please be respectful."
            }
            notification_message = await context.bot.send_message(
                chat_id=chat_id,
                text=notification_message_text.get(reason, "Your message was deleted.")
            )

            temporary_notified_users.add(username_id)
            log_action(f"Notification sent to user {username_id} for reason: {reason}.")
            asyncio.create_task(delete_warning_message(context, chat_id, notification_message.message_id))

    except telegram.error.BadRequest as e:
        logging.error(f"Error notifying user {username_id}: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user messages and checks for language, duplicates, and inappropriate content."""
    try:
        message = update.message
        if not message:
            logging.error("No message found in the update.")
            return

        message_text = message.text or message.caption or ''
        user = message.from_user
        if not user:
            logging.error("No user found in the message.")
            return

        username_id = f"@{user.username}" if user.username else f"@{user.id}"
        chat_id = message.chat_id
        current_time = time.time()

        # Admin check
        if str(user.id) == ID_ADMIN:
            logging.info("Message from admin, filters ignored.")
            return

        # Language and inappropriate content check
        words = re.sub(r'http[s]?://\S+', '', message_text).split()
        contains_profanity = any(profanity.contains_profanity(word) for word in words if word.lower() not in authorized_words)

        if contains_profanity:
            await notify_user_once(context, chat_id, user.username, username_id, reason="inappropriate_language")
            await context.bot.delete_message(chat_id, message.message_id)
            return

        # Check for duplicate messages
        duplicate_text_found = False
        cleaned_text = re.sub(r'http[s]?://\S+', '', message_text).strip()
        for stored_text, timestamp in recent_messages.get(chat_id, []):
            if stored_text == cleaned_text and (current_time - timestamp) < CHECK_INTERVAL:
                duplicate_text_found = True
                break

        if duplicate_text_found:
            await notify_user_once(context, chat_id, user.username, username_id, reason="duplicate")
            await context.bot.delete_message(chat_id, message.message_id)
            return

        recent_messages.setdefault(chat_id, []).append((cleaned_text, current_time))
        await notify_post(update, context)

    except Exception as e:
        logging.error(f"Error handling message for user {username_id}: {str(e)}")
        await send_error_to_admin(update, context, f"Error for user {username_id}: {str(e)}")

async def notify_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a private message to users after they post in the group."""
    global message_count
    try:
        user = update.message.from_user
        if not user:
            logging.warning("No user found in the message.")
            return

        user_identifier = f"@{user.username}" if user.username else f"@{user.id}"
        message_count += 1

        if message_count % 3 == 0:
            message_to_send = f"Welcome {user_identifier}! Please share our community link to support us."
            keyboard = [
                [InlineKeyboardButton("Share on Telegram", url="https://t.me/share/url?...")],
                [InlineKeyboardButton("Share on WhatsApp", url="https://wa.me/?text=...")],
                [InlineKeyboardButton("Join the community", url="https://t.me/addlist/...")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.message.chat.id, 
                text=message_to_send, 
                reply_markup=reply_markup
            )
            message_count = 0

        notified_users.add(user.id)

    except Exception as e:
        logging.error(f"Error sending notification: {e}")
        await send_error_to_admin(update, context, e)

async def send_group_rules(application):
    """Sends the group rules to the group."""
    chat_id = ID_GROUP
    rules_message = """
📜 Group Rules

1. No spam or duplicate messages.
2. Keep it respectful.
3. Only English messages allowed.

Join the community for access to more resources.
    """
    keyboard = [
        [InlineKeyboardButton("Join the community", url="https://t.me/addlist/...")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await application.bot.send_message(
            chat_id=chat_id, 
            text=rules_message, 
            reply_markup=reply_markup
        )
        log_action("Group rules sent successfully.")
    except Exception as e:
        logging.error(f"Error sending group rules: {e}")
        await send_error_to_admin(application, e)
