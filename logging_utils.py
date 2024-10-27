import logging
from telegram import Bot, Update, Message
from telegram.ext import ContextTypes
from datetime import datetime
from typing import Optional
from config import ID_ADMIN  # Ensure ID_ADMIN is set to the admin's Telegram ID in config.py

def log_action(action: str) -> None:
    """Logs an action with a timestamp."""
    logging.info(f"{action} - {datetime.now()}")

async def send_error_to_admin(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE, message: Optional[Message] = None, reason: str = ""):
    """Sends an error or warning message to the admin and forwards the deleted message if available."""
    bot = context.bot
    admin_chat_id = ID_ADMIN
    
    # Construct a warning message with the reason if provided
    warning_message = f"⚠️ A message was deleted.\nReason: {reason}\n" if reason else "⚠️ A message was deleted without a specific reason."
    
    # Add update information if available
    if update and isinstance(update, Update):
        warning_message += f"\nUpdate: {update.to_dict()}"

    # Send the warning message to the admin
    try:
        await bot.send_message(chat_id=admin_chat_id, text=warning_message)
    except Exception as e:
        logging.error(f"Error sending warning message to admin: {e}")

    # Forward the deleted message to the admin if available
    if message:
        try:
            # Send text or caption if present
            if message.text or message.caption:
                await bot.send_message(chat_id=admin_chat_id, text=message.text or message.caption)

            # Forward media files if present
            if message.photo:
                await bot.send_photo(chat_id=admin_chat_id, photo=message.photo[-1].file_id, caption=message.caption or "")

            if message.video:
                await bot.send_video(chat_id=admin_chat_id, video=message.video.file_id, caption=message.caption or "")

            if message.audio:
                await bot.send_audio(chat_id=admin_chat_id, audio=message.audio.file_id, caption=message.caption or "")

            if message.document:
                await bot.send_document(chat_id=admin_chat_id, document=message.document.file_id, caption=message.caption or "")

            log_action(f"Message from {message.from_user.username or message.from_user.id} forwarded to admin.")
        
        except Exception as e:
            logging.error(f"Error forwarding message to admin: {e}")
