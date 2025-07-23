import asyncio
import re
from typing import Optional
from highrise import *
from config import AUTHORIZED_USERS, SPAM_COUNT, DANCE_REPEAT_DELAY, SPAM_DELAY
from dances import get_dance_by_number, get_all_dances

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.spam_active = False
        self.dance_active = False
        
    def is_authorized(self, user_id: str) -> bool:
        """Check if user is authorized for admin commands"""
        return user_id in AUTHORIZED_USERS
    
    async def handle_come_bot(self, user: User, message: str):
        """Handle 'come bot' command - teleport bot to user"""
        if not self.is_authorized(user.username):
            return
            
        if "come bot" in message.lower():
            try:
                # Get user's position
                user_position = await self.bot.highrise.get_user_position(user.id)
                if user_position:
                    # Teleport bot to user's position
                    await self.bot.highrise.teleport(self.bot.highrise.my_id, user_position.position)
                    await self.bot.highrise.chat(f"🤖 Coming to {user.username}!")
            except Exception as e:
                await self.bot.highrise.chat("❌ Failed to teleport to user")
    
    async def handle_dance_command(self, user: User, message: str):
        """Handle individual dance commands (numbers 1-100)"""
        # Check if message is just a number
        if message.strip().isdigit():
            dance_number = int(message.strip())
            if 1 <= dance_number <= 100:
                dance_animation = get_dance_by_number(dance_number)
                try:
                    await self.bot.highrise.send_emote(dance_animation, user.id)
                    await self.bot.highrise.chat(f"💃 {user.username} is performing dance #{dance_number}!")
                except Exception as e:
                    await self.bot.highrise.chat(f"❌ Failed to execute dance for {user.username}")
    
    async def handle_tip_all(self, user: User, message: str):
        """Handle 'tipall1' command - tip 1 gold to all users"""
        if not self.is_authorized(user.username):
            return
            
        if "tipall1" in message.lower():
            try:
                # Get bot's gold balance
                wallet = await self.bot.highrise.get_wallet()
                if wallet.gold < 1:
                    await self.bot.highrise.chat("❌ ربات گلد نداره")
                    return
                
                # Get all users in room
                room_users = await self.bot.highrise.get_room_users()
                users_tipped = 0
                
                for room_user, position in room_users.content:
                    if room_user.id != self.bot.highrise.my_id:  # Don't tip self
                        try:
                            await self.bot.highrise.tip_user(room_user.id, "gold_bar_1")
                            await self.bot.highrise.chat(f"کاربر {room_user.username} 1 گلد دریافت کرد 👑🟡✅")
                            users_tipped += 1
                            await asyncio.sleep(0.5)  # Prevent rate limiting
                        except Exception as e:
                            continue
                
                if users_tipped == 0:
                    await self.bot.highrise.chat("❌ No users to tip")
                    
            except Exception as e:
                await self.bot.highrise.chat("❌ Failed to process tip command")
    
    async def handle_spam_command(self, user: User, message: str):
        """Handle spam commands - repeat message 100 times"""
        if not self.is_authorized(user.username):
            return
            
        # Check for spam command patterns
        spam_patterns = [
            r"spam\s+(.+)",  # "spam hello"
            r"(.+)\s+spam"   # "hello spam"
        ]
        
        spam_text = None
        for pattern in spam_patterns:
            match = re.search(pattern, message.lower())
            if match:
                spam_text = match.group(1).strip()
                break
        
        if spam_text and spam_text != "stop":
            self.spam_active = True
            await self.bot.highrise.chat(f"🔄 Starting spam: '{spam_text}'")
            
            for i in range(SPAM_COUNT):
                if not self.spam_active:  # Check if stopped
                    break
                await self.bot.highrise.chat(spam_text)
                await asyncio.sleep(SPAM_DELAY)
            
            if self.spam_active:
                await self.bot.highrise.chat("✅ Spam completed (100 messages)")
            self.spam_active = False
    
    async def handle_dance_all_command(self, user: User, message: str):
        """Handle 'dance all [number]' command - make everyone dance"""
        if not self.is_authorized(user.username):
            return
            
        match = re.search(r"dance all\s+(\d+)", message.lower())
        if match:
            dance_number = int(match.group(1))
            if 1 <= dance_number <= 100:
                try:
                    room_users = await self.bot.highrise.get_room_users()
                    dance_animation = get_dance_by_number(dance_number)
                    
                    for room_user, position in room_users.content:
                        if room_user.id != self.bot.highrise.my_id:
                            try:
                                await self.bot.highrise.send_emote(dance_animation, room_user.id)
                                await asyncio.sleep(0.2)
                            except:
                                continue
                    
                    await self.bot.highrise.chat(f"💃 Everyone is performing dance #{dance_number}!")
                    
                except Exception as e:
                    await self.bot.highrise.chat("❌ Failed to execute group dance")
    
    async def handle_dance_bot_command(self, user: User, message: str):
        """Handle 'dance bot [number]' command - make bot dance repeatedly"""
        if not self.is_authorized(user.username):
            return
            
        match = re.search(r"dance bot\s+(\d+)", message.lower())
        if match:
            dance_number = int(match.group(1))
            if 1 <= dance_number <= 100:
                self.dance_active = True
                dance_animation = get_dance_by_number(dance_number)
                
                await self.bot.highrise.chat(f"🤖 Bot performing dance #{dance_number} (repeating)")
                
                while self.dance_active:
                    try:
                        await self.bot.highrise.send_emote(dance_animation, self.bot.highrise.my_id)
                        await asyncio.sleep(DANCE_REPEAT_DELAY)
                    except:
                        break
                
                if not self.dance_active:
                    await self.bot.highrise.chat("⏹️ Bot dance stopped")
    
    async def handle_stop_command(self, user: User, message: str):
        """Handle 'stop' command - stop spam or dance loops"""
        if not self.is_authorized(user.username):
            return
            
        if message.lower().strip() == "stop":
            if self.spam_active:
                self.spam_active = False
                await self.bot.highrise.chat("⏹️ Spam stopped")
            
            if self.dance_active:
                self.dance_active = False
                await self.bot.highrise.chat("⏹️ Dance stopped")
    
    async def process_message(self, user: User, message: str):
        """Process all incoming messages and handle commands"""
        # Handle all command types
        await self.handle_come_bot(user, message)
        await self.handle_dance_command(user, message)
        await self.handle_tip_all(user, message)
        await self.handle_spam_command(user, message)
        await self.handle_dance_all_command(user, message)
        await self.handle_dance_bot_command(user, message)
        await self.handle_stop_command(user, message)
