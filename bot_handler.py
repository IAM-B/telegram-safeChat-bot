import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder, CallbackContext
from config import ID_ADMIN  # Ensure ID_ADMIN is set to the admin's Telegram ID in config.py

# Function to notify admin of a new user interaction with the bot
async def notify_admin_new_user(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_info = f"""
*New user interaction with bot*:
- Username: @{user.username if user.username else 'Unknown'}
- First name: {user.first_name}
- Last name: {user.last_name if user.last_name else 'Unknown'}
- User ID: {user.id}
    """
    # Send a message to the admin with the user's info
    await context.bot.send_message(chat_id=ID_ADMIN, text=user_info, parse_mode='Markdown')

# Function called when the user types /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username = f"@{user.username}" if user.username else ""
    
    # Welcome message
    message = "Welcome! This bot offers various services. Please select an option below:"

    # Create an interactive keyboard with buttons
    keyboard = [
        [InlineKeyboardButton("Option 1", url="https://...")],
        [InlineKeyboardButton("Option 2", url="https://...")]
    ]

    # Set up the keyboard layout
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message with options
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

    # Notify admin of new user interaction
    await notify_admin_new_user(update, context)

# Function for /help
async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = """
*Available commands:*

/start - Start interacting with the bot
/help - Display this help message
/rules - Show the group rules
    """
    await update.message.reply_text(help_message, parse_mode="Markdown")

# Function for /rules
async def rules_command(update: Update, context: CallbackContext) -> None:
    rules_message = """
*Group Rules*:
1. Be respectful.
2. No spamming.
3. Follow the group's topic.
    """
    await update.message.reply_text(rules_message, parse_mode="Markdown")

# Function for /suggest (submit a suggestion)
async def dev_command(update: Update, context: CallbackContext) -> None:
    suggest_message = """
We value your feedback! Please use the button below to submit a suggestion.
"""
    keyboard = [
        [InlineKeyboardButton("Submit Suggestion", url="https://...")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(suggest_message, reply_markup=reply_markup, parse_mode="Markdown")

# Function for /post (post an announcement)
async def post_command(update: Update, context: CallbackContext) -> None:
    post_message = "🛒 *Post an announcement*: Please provide details of your announcement (title, price, description, contact information)."
    await update.message.reply_text(post_message, parse_mode="Markdown")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
