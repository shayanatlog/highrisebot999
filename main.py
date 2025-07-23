#!/usr/bin/env python3
import asyncio
import sys
import os
from bot import main as bot_main
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "ربات روشنه در Render!"

def check_environment():
    bot_token = os.getenv("HIGHRISE_BOT_TOKEN")
    room_id = os.getenv("HIGHRISE_ROOM_ID")
    
    if not bot_token:
        print("❌ HIGHRISE_BOT_TOKEN تنظیم نشده")
        return False
    if not room_id:
        print("❌ HIGHRISE_ROOM_ID تنظیم نشده")
        return False
    return True

def print_welcome():
    print("=" * 60)
    print("🤖 HIGHRISE BOT - STARTING...")
    print("=" * 60)

def run_bot():
    try:
        asyncio.run(bot_main())
    except Exception as e:
        print(f"❌ Bot crash: {e}")

if __name__ == "__main__":
    print_welcome()
    if not check_environment():
        sys.exit(1)
    
    # اجرای ربات در Thread جدا
    threading.Thread(target=run_bot).start()
    
    # اجرای Flask برای زنده نگه‌داشتن سرور
    app.run(host="0.0.0.0", port=8080)
