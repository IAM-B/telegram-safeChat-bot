# Telegram Bot for Group Moderation and Community Engagement

This is a custom Telegram bot designed for group moderation, user notification, and community management. It includes automated message filtering, duplicate detection, profanity checking, and scheduled reminders.

## Features

- **Message Moderation**: Automatically detects and removes inappropriate language, duplicate messages, and messages in unauthorized languages.
- **Deleted Message Tracking**: Sends information about deleted messages to the admin, providing details on the user and reason for deletion.
- **User Notifications**: Sends custom warnings to users when their messages are flagged for violations.
- **Group Rules Reminder**: Automatically posts group rules daily at a specified time.
- **Community Engagement**: Periodically sends prompts for users to share the group, helping to grow the community.
- **Manual Update Notifications**: Allows the admin to manually notify the group of a new bot update using a notification script.

## Requirements

- **Python 3.7+**
- **Telegram Bot Token**: Obtainable via the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
- **Dependencies**: Listed in `requirements.txt`. Install them with:
  ```bash
  pip install -r requirements.txt
  ```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/IAM-B/telegram-safeChat-bot.git
   cd telegram-safeChat-bot
   ```

2. **Set Up Configuration**:
   - Create a `config.py` file with the following variables:
     ```python
     TOKEN = 'your_bot_token'
     ID_GROUP = 'your_group_id'
     ID_ADMIN = 'your_admin_id'
     CHECK_INTERVAL = 43200  # Time in seconds to check for duplicate messages
     ```
   - Replace `'your_bot_token'`, `'your_group_id'`, and `'your_admin_id'` with actual values.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Manual Bot Update Notification (Optional)**:
   - Admins can run the `notify_update.sh` script manually to notify the group of a new bot update:
     ```bash
     ./notify_update.sh
     ```

## Usage

### Starting the Bot
Run the bot with:
```bash
python main.py
```

### Available Commands

- `/start` - Begins interaction with the bot.
- `/help` - Provides a list of available commands.
- `/rules` - Displays the group rules.
- `/dev` - Sends a message to get in touch with the developers.
- `/post` - Posts an announcement in the group (for admins).

### Bot Functionalities

1. **Duplicate Message Detection**:
   - The bot checks for duplicate messages, images, and videos within a specified interval (set by `CHECK_INTERVAL`).
   - Users are notified if they send duplicate content.

2. **Language Filtering**:
   - Only messages in English are allowed.
   - Messages in other languages are removed, and users are notified.

3. **Profanity Detection**:
   - The bot automatically censors messages containing inappropriate language using the `better_profanity` library.

4. **Deleted Message Tracking**:
   - Every time a message is deleted for violating group rules, the bot sends a notification to the admin with details such as:
     - The user’s ID or username.
     - The reason for deletion (e.g., duplicate, inappropriate language).
     - A copy of the original message if it contained text, or information about the type of content deleted (photo, video, etc.).

5. **Daily Group Rules Reminder**:
   - The bot posts group rules daily at a scheduled time to remind users of acceptable behavior.

6. **Community Sharing Prompt**:
   - Periodically, the bot sends a prompt for users to share the group link to help grow the community.

7. **Manual Update Notifications**:
   - The admin can run the `notify_update.sh` script manually to notify the group of any new updates.

## Deployment on Railway

To deploy this bot on [Railway](https://railway.app/), follow these steps:

1. **Create a Railway Account and New Project**:
   - Sign up or log in to Railway.
   - Create a new project.

2. **Set Up Environment Variables**:
   - In the Railway dashboard, go to the project’s settings.
   - Add the following environment variables (these will replace `config.py`):
     - `TOKEN`: Your Telegram bot token.
     - `ID_GROUP`: The group ID where the bot will operate.
     - `ID_ADMIN`: The admin’s Telegram ID for receiving notifications.
     - `CHECK_INTERVAL`: The interval for duplicate message checking in seconds (e.g., `43200`).

3. **Deploy the Code**:
   - In the Railway project, link the GitHub repository containing your bot.
   - In the `Start Command` field in Railway, set the command to:
     ```bash
     python main.py
     ```

4. **Start the Bot**:
   - Deploy the project, and Railway will start your bot automatically.
   - Logs and any errors will be viewable directly from the Railway dashboard.

## Logging

The bot uses a logging system to track actions and errors, which helps with debugging and ensures smooth operation. Logs are saved to `bot.log`.

## Contributing

Contributions are welcome! If you would like to improve this bot, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or support, feel free to reach out to the bot administrators or open an issue in this repository.

---

### Notes

1. **Security Advice**:
   - Never share your `TOKEN` or `ID_ADMIN` publicly. For cloud deployments, use environment variables.

2. **Scheduling**:
   - The bot uses `APScheduler` for daily tasks. Ensure your hosting environment supports asynchronous scheduling.
