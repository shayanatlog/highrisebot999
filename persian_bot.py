#!/usr/bin/env python3
"""
ربات هایگرایز فارسی با تمام قابلیت های درخواستی
Persian Highrise Bot with all requested features
"""
from keep_alive import keep_alive
keep_alive()

import asyncio
from highrise import BaseBot, User, Position
import os
import re

class HighriseBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.spam_active = False
        self.dance_active = False
        self.continuous_dance_active = False
        self.continuous_dance_number = 1
        self.individual_continuous_dances = {}  # {user_id: dance_number}
        self.authorized_users = ["Robot.NM", "389._.20"]

        # دنس های خفن که کار می‌کنند
        awesome_emotes = [
            "emote-wave", "emote-clap", "emote-thumbsup", "emote-laugh", "emote-heart", 
            "emote-bow", "emote-peace", "emote-cute", "emote-angry", "emote-confused",
            "idle-dance-casual", "emote-kiss", "emote-cry", "emote-sleep", "emote-wake",
            "emote-roll", "emote-backflip", "emote-cartwheel", "emote-headstand", "emote-split"
        ]

        # ساخت ۱۰۰ دنس خفن
        self.dances = {}
        for i in range(1, 101):
            self.dances[i] = awesome_emotes[(i-1) % len(awesome_emotes)]

        # دنس های خاص درخواستی با کدهای دقیق
        self.dances[1] = "emote-ghost-idle"     # Ghost dance
        self.dances[2] = "idle_layingdown2"     # Laying down 2
        self.dances[3] = "idle-sleep"           # #CozyNap - دنس نشست
        self.dances[4] = "emote-attentive"       # #TwerkItOut
        self.dances[5] = "idle-loop-sitfloor"   # #Rest - دنس نشست که ۵ هزار گلده
        self.dances[6] = "emote-bow"            # #Proposing

    async def on_start(self, session_metadata):
        print("🤖 ربات با موفقیت شروع شد!")
        await self.highrise.chat("🤖 ربات فعال شد و آماده خدمت است!")

    async def on_chat(self, user: User, message: str):
        print(f"💬 {user.username}: {message}")

        # دستور دنس با اعداد ۱-۱۰۰
        if message.strip().isdigit():
            dance_number = int(message.strip())
            if 1 <= dance_number <= 100:
                # اگر کاربر قبلاً دنس دیگری داشته، متوقف کن و جدید شروع کن
                self.individual_continuous_dances[user.id] = dance_number
                asyncio.create_task(self.individual_continuous_dance_loop(user.id, dance_number))

        # دستور come bot برای کاربران مجاز
        elif "come bot" in message.lower() and user.username in self.authorized_users:
            try:
                room_users_response = await self.highrise.get_room_users()
                user_position = None

                if hasattr(room_users_response, 'content') and room_users_response.content:
                    for room_user, position in room_users_response.content:
                        if room_user.id == user.id:
                            user_position = position
                            break

                if user_position:
                    await self.highrise.teleport(self.highrise.my_id, user_position)
                    await self.highrise.chat(f"🤖 در حال آمدن نزد {user.username}!")
                else:
                    await self.highrise.chat("❌ نتوانستم موقعیت شما را پیدا کنم")

            except Exception as e:
                print(f"Teleport error: {e}")
                await self.highrise.chat("❌ خطا در انتقال ربات")

        # دستور tipall1 برای کاربران مجاز
        elif "tipall1" in message.lower() and user.username in self.authorized_users:
            try:
                wallet_response = await self.highrise.get_wallet()
                room_users_response = await self.highrise.get_room_users()
                users_tipped = 0

                if hasattr(room_users_response, 'content') and room_users_response.content:
                    for room_user, position in room_users_response.content:
                        if room_user.id != self.highrise.my_id:
                            try:
                                await self.highrise.tip_user(room_user.id, "gold_bar_1")
                                await self.highrise.chat(f"کاربر {room_user.username} 1 گلد دریافت کرد 👑🟡✅")
                                users_tipped += 1
                                await asyncio.sleep(0.5)
                            except Exception as e:
                                continue

                if users_tipped == 0:
                    await self.highrise.chat("❌ کاربری برای تیپ یافت نشد")

            except Exception as e:
                print(f"Tip error: {e}")
                await self.highrise.chat("❌ خطا در پردازش دستور تیپ")

        # دستور heart all برای ارسال قلب همزمان به همه
        elif "heart all" in message.lower() and user.username in self.authorized_users and "rep" not in message.lower():
            try:
                room_users_response = await self.highrise.get_room_users()
                if hasattr(room_users_response, 'content') and room_users_response.content:
                    for room_user, position in room_users_response.content:
                        if room_user.id != self.highrise.my_id:
                            try:
                                await self.highrise.react("heart", room_user.id)
                                await asyncio.sleep(0.1)
                            except:
                                continue
                    await self.highrise.chat("💓 قلب برای همه ارسال شد!")
            except Exception as e:
                await self.highrise.chat("❌ خطا در ارسال قلب")

        # دستور heart all rep برای ارسال قلب یکی یکی با پیام
        elif "heart all rep" in message.lower() and user.username in self.authorized_users:
            try:
                room_users_response = await self.highrise.get_room_users()
                if hasattr(room_users_response, 'content') and room_users_response.content:
                    for room_user, position in room_users_response.content:
                        if room_user.id != self.highrise.my_id:
                            try:
                                await self.highrise.react("heart", room_user.id)
                                await self.highrise.chat(f"کاربر {room_user.username} یک قلب گرفت ❤️💓")
                                await asyncio.sleep(1.0)
                            except:
                                continue
            except Exception as e:
                await self.highrise.chat("❌ خطا در ارسال قلب")

        # دستور walet برای نمایش موجودی گلد ربات
        elif "walet" in message.lower() and user.username in self.authorized_users:
            try:
                wallet_response = await self.highrise.get_wallet()
                print(f"Wallet response type: {type(wallet_response)}")
                print(f"Wallet response content: {wallet_response}")

                gold_amount = 0
                if hasattr(wallet_response, 'content') and wallet_response.content:
                    for currency_item in wallet_response.content:
                        if hasattr(currency_item, 'type') and currency_item.type == 'gold':
                            gold_amount = currency_item.amount
                            break

                await self.highrise.chat(f"💰 ربات {gold_amount} گلد داره 🟡")
                print(f"Gold amount found and shown: {gold_amount}")
            except Exception as e:
                print(f"Wallet error: {e}")
                await self.highrise.chat("❌ خطا در دریافت اطلاعات کیف پول")

        # بررسی دستورات کاربران مجاز
        elif user.username in self.authorized_users:
            # دستور spam
            spam_patterns = [r"spam\s+(.+)", r"(.+)\s+spam"]
            spam_text = None
            for pattern in spam_patterns:
                match = re.search(pattern, message)
                if match:
                    spam_text = match.group(1).strip()
                    break

            if spam_text and spam_text != "stop":
                self.spam_active = True
                await self.highrise.chat(f"🔄 شروع spam: '{spam_text}' - ۱۰۰ بار")

                count = 0
                for i in range(100):
                    if not self.spam_active:
                        break
                    try:
                        await self.highrise.chat(spam_text)
                        count += 1
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        print(f"Spam error at {count}: {e}")
                        await asyncio.sleep(1.0)
                        continue

                if self.spam_active:
                    await self.highrise.chat(f"✅ spam تکمیل شد ({count} پیام)")
                self.spam_active = False

            # دستور dance all یا danceall
            elif "dance all" in message.lower() or "danceall" in message.lower():
                match = re.search(r"(?:dance all|danceall)\s*(\d+)", message.lower())
                if match:
                    dance_number = int(match.group(1))
                    if 1 <= dance_number <= 100:
                        try:
                            room_users_response = await self.highrise.get_room_users()
                            dance_animation = self.dances.get(dance_number, "emote-float")

                            if hasattr(room_users_response, 'content') and room_users_response.content:
                                for room_user, position in room_users_response.content:
                                    try:
                                        await self.highrise.send_emote(dance_animation, room_user.id)
                                        await asyncio.sleep(0.1)
                                    except:
                                        continue

                            await self.highrise.chat(f"💃 همه با هم می‌رقصند! دنس شماره {dance_number}")

                        except Exception as e:
                            await self.highrise.chat("❌ خطا در اجرای دنس گروهی")

            # دستور dance bot
            elif "dance bot" in message.lower():
                match = re.search(r"dance bot\s+(\d+)", message.lower())
                if match:
                    dance_number = int(match.group(1))
                    if 1 <= dance_number <= 100:
                        self.dance_active = True
                        dance_animation = self.dances.get(dance_number, "emote-wave")

                        await self.highrise.chat(f"🤖 ربات در حال اجرای دنس شماره {dance_number} (تکراری)")

                        while self.dance_active:
                            try:
                                await self.highrise.send_emote(dance_animation, self.highrise.my_id)
                                await asyncio.sleep(2.0)
                            except:
                                break

                        if not self.dance_active:
                            await self.highrise.chat("⏹️ دنس ربات متوقف شد")

            # دستور stop
            elif message.lower().strip() == "stop":
                if self.spam_active:
                    self.spam_active = False
                    await self.highrise.chat("⏹️ spam متوقف شد")

                if self.dance_active:
                    self.dance_active = False
                    await self.highrise.chat("⏹️ دنس متوقف شد")

                if self.continuous_dance_active:
                    self.continuous_dance_active = False
                    await self.highrise.chat("⏹️ دنس مداوم متوقف شد")

                # متوقف کردن دنس مداوم فردی
                if user.id in self.individual_continuous_dances:
                    del self.individual_continuous_dances[user.id]

    async def on_user_join(self, user: User, position):
        print(f"➕ {user.username} وارد اتاق شد")
        await self.highrise.chat(f"سلام {user.username}! به روم B2 خوش اومدی! برای دنس از ۱ تا ۱۰۰ استفاده کنید و برای خاموش کردن دنس stop بزنید")

    async def on_user_leave(self, user: User):
        print(f"➖ {user.username} از اتاق خارج شد")

    async def individual_continuous_dance_loop(self, user_id: str, dance_number: int):
        """دنس مداوم برای یک کاربر خاص"""
        while user_id in self.individual_continuous_dances and self.individual_continuous_dances[user_id] == dance_number:
            try:
                dance_animation = self.dances.get(dance_number, "emote-wave")
                await self.highrise.send_emote(dance_animation, user_id)
                await asyncio.sleep(4.0)
            except Exception as e:
                print(f"Individual continuous dance error for user {user_id}: {e}")
                await asyncio.sleep(2.0)

async def main():
    bot_token = os.getenv("HIGHRISE_BOT_TOKEN", "68495405d4fb68f4a423ff092cc4157f5a11b95bdbd8e1fd989b3602a56ea13c")
    room_id = "687d5f34b342b9609d827132"  # آیدی اتاق به صورت ثابت

    print("🚀 شروع ربات هایگرایز...")
    print(f"🔑 استفاده از توکن: {bot_token[:10]}...")
    print(f"🏠 اتاق هدف: {room_id}")

    bot = HighriseBot()

    from highrise.__main__ import main as cli_main
    from highrise.__main__ import BotDefinition

    definition = BotDefinition(bot=bot, room_id=room_id, api_token=bot_token)
    await cli_main([definition])

if __name__ == "__main__":
    asyncio.run(main())
