"""
🎓 SI STUDENT ACCOUNT - টেলিগ্রাম বট মেইন
bot/main.py

টেলিগ্রাম বট এন্ট্রি পয়েন্ট
"""

import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler, filters
)
from config.settings import TELEGRAM_BOT_TOKEN
from database.db import db
from .handlers import StudentHandlers

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# কথোপকথন স্টেট
from .handlers import (
    REGISTRATION_COUNTRY, REGISTRATION_EMAIL, REGISTRATION_PASSWORD,
    REGISTRATION_CONFIRM_PASSWORD, REGISTRATION_FIRST_NAME, REGISTRATION_LAST_NAME,
    REGISTRATION_PHONE, REGISTRATION_GENDER, REGISTRATION_UNIVERSITY,
    REGISTRATION_STUDENT_ID, REGISTRATION_DEGREE, REGISTRATION_CONFIRM,
    LOGIN_EMAIL, LOGIN_PASSWORD
)


class TelegramBot:
    """টেলিগ্রাম বট ক্লাস"""
    
    def __init__(self):
        self.application = None
    
    async def initialize(self):
        """
        বট ইনিশিয়ালাইজ করুন
        """
        logger.info("🤖 টেলিগ্রাম বট শুরু হচ্ছে...")
        
        # ডাটাবেস সংযোগ
        db.connect()
        db.initialize_schema()
        
        # অ্যাপ্লিকেশন তৈরি করুন
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # কমান্ড হ্যান্ডেলার
        self.application.add_handler(CommandHandler("start", StudentHandlers.start))
        self.application.add_handler(CommandHandler("help", StudentHandlers.help_command))
        
        # রেজিস্ট্রেশন কথোপকথন হ্যান্ডেলার
        registration_conv_handler = ConversationHandler(
            entry_points=[MessageHandler(filters.Regex(r"^📝 রেজিস্ট্রেশন$"), StudentHandlers.start_registration)],
            states={
                REGISTRATION_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_country)],
                REGISTRATION_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_email)],
                REGISTRATION_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_password)],
                REGISTRATION_CONFIRM_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_confirm_password)],
                REGISTRATION_FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_first_name)],
                REGISTRATION_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_last_name)],
                REGISTRATION_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_phone)],
                REGISTRATION_UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_university)],
                REGISTRATION_STUDENT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_student_id)],
                REGISTRATION_DEGREE: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_degree)],
                REGISTRATION_GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_gender)],
                REGISTRATION_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, StudentHandlers.registration_confirm)],
            },
            fallbacks=[CommandHandler('cancel', StudentHandlers.cancel)]
        )
        
        self.application.add_handler(registration_conv_handler)
        
        # মেনু হ্যান্ডেলার
        self.application.add_handler(
            MessageHandler(filters.Regex(r"^(📝 রেজিস্ট্রেশন|🔐 লগইন|💰 ক্রেডিট লোড|📊 ব্যালেন্স দেখুন|📧 ইনবক্স|🎯 কাজ সমূহ|⚙️ সেটিংস|ℹ️ সাহায্য)$"), StudentHandlers.help_command)
        )
        
        logger.info("✅ বট সফলভাবে ইনিশিয়ালাইজ হয়েছে")
    
    async def start(self):
        """
        বট চালু করুন
        """
        await self.initialize()
        logger.info("🚀 বট চলছে...")
        await self.application.run_polling()
    
    async def stop(self):
        """
        বট বন্ধ করুন
        """
        db.disconnect()
        logger.info("🛑 বট বন্ধ হয়েছে")


def create_bot():
    """বট তৈরি করুন"""
    return TelegramBot()
