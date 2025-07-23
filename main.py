#!/usr/bin/env python3
"""
Highrise Bot with Dance Commands, Gold Tipping, Spam Messaging, and Teleportation
Created for authorized users with comprehensive command system.
"""

from flask import Flask
from threading import Thread
import asyncio
import sys
import os
from bot import main  # فرض می‌کنیم در bot.py تابع main وجود داره
from config import HIGHRISE_BOT_TOKEN, HIGHRISE_ROOM_ID  # فرض کنید در config.py این متغیرها قرار دارن

# تعریف اپلیکیشن Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "ربات روشنه در Render!"

# تابع راه‌اندازی سرور Flask
def run_flask():
    # می‌توانید پورت مورد نظر را تغییر دهید؛ اینجا 8080 است.
    app.run(host="0.0.0.0", port=8080)

# توابع کمکی
def check_environment():
    """بررسی تنظیمات محیط"""
    bot_token = os.getenv("HIGHRISE_BOT_TOKEN", HIGHRISE_BOT_TOKEN)
    room_id = os.getenv("HIGHRISE_ROOM_ID", HIGHRISE_ROOM_ID)
    
    if not bot_token:
        print("❌ ERROR: HIGHRISE_BOT_TOKEN environment variable not set")
        return False
    
    if not room_id:
        print("❌ ERROR: HIGHRISE_ROOM_ID environment variable not set")
        return False
    
    return True

def print_welcome():
    """پیام خوشامدگویی و معرفی امکانات"""
    print("=" * 60)
    print("🤖 HIGHRISE BOT - ADVANCED FEATURES")
    print("=" * 60)
    print("📋 Bot Features:")
    print("  • Teleportation: 'come bot' (authorized users only)")
    print("  • Dance System: Type numbers 1-100 for unique dances")
    print("  • Gold Tipping: 'tipall1' to tip everyone (authorized users)")
    print("  • Spam Messages: 'spam [message]' repeats 100 times")
    print("  • Group Dances: 'dance all [number]' for everyone")
    print("  • Bot Dances: 'dance bot [number]' with repeat")
    print("  • Stop Commands: 'stop' to halt spam/dance loops")
    print("=" * 60)

def run_bot():
    """راه‌اندازی بات Highrise"""
    print_welcome()
    if not check_environment():
        sys.exit(1)
    try:
        print("🔄 Initializing bot...")
        # این قسمت تابع main بات رو اجرا می‌کنه (با asyncio)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        sys.exit(1)

# نقطه ورود اصلی
if __name__ == "__main__":
    # شروع سرور Flask در یک ترد جدا
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # اجرای بات Highrise
    run_bot()
