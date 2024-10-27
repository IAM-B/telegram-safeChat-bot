import asyncio
import logging
from config import TOKEN, CHECK_INTERVAL
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from bot_handler import start, rules_command, dev_command, help_command, post_command
from message_handler import notify_post, handle_message, reset_notified_users, schedule_daily_rules
from logging_utils import send_error_to_admin


def main() -> None:
    logging.info("Bot is starting")
    application = Application.builder().token(TOKEN).build()

    # Adding command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("dev", dev_command))
    application.add_handler(CommandHandler("post", post_command))

    # Adjust filters here to manage different types of messages based on content
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Handlers for media files (photos, videos, audio)
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.AUDIO, handle_message))

    # Error handler for logging and notification to admin
    application.add_error_handler(lambda update, context: send_error_to_admin(update, context, context.error))

    # Schedule daily rules message
    schedule_daily_rules(application)

    # Start the bot
    application.run_polling()
    logging.info("Bot is running")

if __name__ == '__main__':
    asyncio.run(main())
