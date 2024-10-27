import sys
from collections import defaultdict
from better_profanity import profanity
from logging import basicConfig, INFO, StreamHandler, FileHandler

# Configuration variables (set these in an external config file for security)
TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token or set in config
ID_GROUP = "YOUR_GROUP_ID"  # Replace with your group ID or set in config
ID_GROUP_TEST = "YOUR_TEST_GROUP_ID"  # Replace with your test group ID or set in config
ID_ADMIN = "YOUR_ADMIN_ID"  # Replace with your admin ID or set in config
CHECK_INTERVAL = 43200  # in seconds (12 hours)
WAIT_TIME = 60  # in seconds

# Data structures for bot operations
recent_messages = defaultdict(list)
warning_messages = defaultdict(list)
toggle_message_content = {}
notified_users = {}
participant_counter = 1
user_waiting_info = {}

# Load profanity filter
profanity.load_censor_words()

# Logging configuration
basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        StreamHandler(sys.stdout),
        FileHandler('bot.log')
    ]
)

# Writing configuration variables to an external shell script (useful for deployment)
with open("vars.sh", "w") as f:
    f.write(f'TOKEN="{TOKEN}"\n')
    f.write(f'ID_GROUP="{ID_GROUP}"\n')
    f.write(f'ID_ADMIN="{ID_ADMIN}"\n')

print("Configuration and logging initialized successfully.")
