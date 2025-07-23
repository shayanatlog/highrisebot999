#!/usr/bin/env python3
"""
Highrise Bot with Dance Commands, Gold Tipping, Spam Messaging, and Teleportation
Created for authorized users with comprehensive command system.
"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "ربات روشنه در Koyeb!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

import asyncio
import sys
import os
from bot import main

def check_environment():
    """Check if required environment variables are set"""
    bot_token = os.getenv("HIGHRISE_BOT_TOKEN")
    room_id = os.getenv("HIGHRISE_ROOM_ID")
    
    if not bot_token:
        print("❌ ERROR: HIGHRISE_BOT_TOKEN environment variable not set")
        print("Please set your bot token: export HIGHRISE_BOT_TOKEN='your_token_here'")
        return False
    
    if not room_id:
        print("❌ ERROR: HIGHRISE_ROOM_ID environment variable not set")
        print("Please set your room ID: export HIGHRISE_ROOM_ID='your_room_id_here'")
        return False
    
    return True

def print_welcome():
    """Print welcome message and bot features"""
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
    print("")
    print("👥 Authorized Users:")
    print("  • @Robot.NM")
    print("  • @389._.20")
    print("")
    print("💃 Special Dances:")
    print("  • 1 = Relaxed")
    print("  • 2 = GhostFloat")
    print("  • 3 = CozyNap")
    print("  • 4 = TwerkItOut")
    print("  • 5-100 = Various unique animations")
    print("=" * 60)

def main_entry():
    """Main entry point"""
    print_welcome()
    
    if not check_environment():
        sys.exit(1)
    
    try:
        print("🔄 Initializing bot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main_entry()
