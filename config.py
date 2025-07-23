import os

# Bot configuration
BOT_TOKEN = os.getenv("HIGHRISE_BOT_TOKEN", "your_bot_token_here")
ROOM_ID = os.getenv("HIGHRISE_ROOM_ID", "your_room_id_here")

# Authorized user IDs for admin commands
AUTHORIZED_USERS = ["Robot.NM", "389._.20"]

# Bot settings
SPAM_COUNT = 100
DANCE_REPEAT_DELAY = 2.0  # seconds between dance repeats
SPAM_DELAY = 0.5  # seconds between spam messages
