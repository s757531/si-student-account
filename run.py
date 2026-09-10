"""
🎓 SI STUDENT ACCOUNT - মেইন এন্ট্রি পয়েন্ট
run.py

টেলিগ্রাম বট এবং এডমিন প্যানেল শুরু করুন
"""

import asyncio
import sys
from bot.main import create_bot
from config.settings import TELEGRAM_BOT_TOKEN


def main():
    """
    মেইন এন্ট্রি পয়েন্ট
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_bot_token':
        print("""
❌ ত্রুটি: TELEGRAM_BOT_TOKEN সেট করা হয়নি!

.env ফাইল তৈরি করুন এবং আপনার বট টোকেন যোগ করুন:

    cp .env.example .env
    # .env ফাইল এডিট করুন এবং TELEGRAM_BOT_TOKEN যোগ করুন
        """)
        sys.exit(1)
    
    print("""
╔════════════════════════════════════════╗
║ 🎓 SI STUDENT ACCOUNT                  ║
║ টেলিগ্রাম বট শুরু হচ্ছে...             ║
╚════════════════════════════════════════╝
    """)
    
    # বট তৈরি করুন এবং চালু করুন
    bot = create_bot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n\n🛑 বট বন্ধ করা হয়েছে")
        asyncio.run(bot.stop())
    except Exception as e:
        print(f"\n❌ ত্রুটি: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
