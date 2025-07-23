from flask import Flask
import threading
import asyncio
import sys
import os
from bot import main as bot_main
from config import HIGHRISE_BOT_TOKEN, HIGHRISE_ROOM_ID

app = Flask(__name__)

@app.route("/")
def home():
    return "ربات روشنه در Render!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def check_environment():
    bot_token = os.getenv("HIGHRISE_BOT_TOKEN", HIGHRISE_BOT_TOKEN)
    room_id = os.getenv("HIGHRISE_ROOM_ID", HIGHRISE_ROOM_ID)

    if not bot_token:
        print("❌ HIGHRISE_BOT_TOKEN تنظیم نشده")
        return False
    if not room_id:
        print("❌ HIGHRISE_ROOM_ID تنظیم نشده")
        return False
    return True

def print_welcome():
    print("=" * 60)
    print("🤖 HIGHRISE BOT - ADVANCED FEATURES")
    print("=" * 60)
    print("📋 Bot Features:")
    print("  • Teleportation: 'come bot'")
    print("  • Dance: 'dance bot 5'")
    print("  • Spam: 'spam [message]'")
    print("  • Stop: 'stop'")
    print("🤖 STARTING...")
    print("=" * 60)

def run_bot():
    print_welcome()
    if not check_environment():
        sys.exit(1)
    try:
        asyncio.run(bot_main())
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
