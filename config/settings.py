"""
🎓 SI STUDENT ACCOUNT - অ্যাপ্লিকেশন সেটিংস
config/settings.py
"""

import os
from dotenv import load_dotenv

# .env ফাইল লোড করুন
load_dotenv()

# ========================================
# 🤖 TELEGRAM BOT সেটিংস
# ========================================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# ========================================
# 🌐 FLASK ওয়েব সার্ভার
# ========================================
FLASK_APP = os.getenv('FLASK_APP', 'admin_panel/app.py')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# ========================================
# 📊 ডাটাবেস
# ========================================
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/database.db')
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')

# ========================================
# 🔐 এডমিন প্যানেল
# ========================================
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@siaccount.edu')

# ========================================
# 📧 ইমেইল সেটিংস
# ========================================
EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com')
EMAIL_IMAP_PORT = int(os.getenv('EMAIL_IMAP_PORT', 993))
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))

# ========================================
# 💰 পেমেন্ট সেটিংস
# ========================================
PAYMENT_CURRENCY = os.getenv('PAYMENT_CURRENCY', 'USD')
MIN_CREDIT_LOAD = float(os.getenv('MIN_CREDIT_LOAD', 5))
MAX_CREDIT_LOAD = float(os.getenv('MAX_CREDIT_LOAD', 1000))

# ========================================
# 🌍 দেশ সেটিংস
# ========================================
SUPPORTED_COUNTRIES = os.getenv('SUPPORTED_COUNTRIES', 'USA,Bangladesh').split(',')
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# ========================================
# 📝 লগিং
# ========================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'data/logs.txt')

# ========================================
# 📧 শিক্ষা প্রতিষ্ঠানের ডোমেইনস
# ========================================
EDUCATIONAL_DOMAINS = {
    '.edu': 'USA',
    '.ac.bd': 'Bangladesh',
    '.edu.bd': 'Bangladesh',
    '.ac.uk': 'UK',
    '.edu.au': 'Australia'
}

# ========================================
# 📋 অ্যাপ সেটিংস
# ========================================
APP_NAME = 'SI STUDENT ACCOUNT'
APP_VERSION = '1.0.0'
APP_DESCRIPTION = 'Student Management System with Telegram Bot Integration'

if __name__ == "__main__":
    print("🎓 SI STUDENT ACCOUNT - সেটিংস লোড হয়েছে")
    print(f"- Database: {DATABASE_PATH}")
    print(f"- Server: {SERVER_HOST}:{SERVER_PORT}")
    print(f"- Admin User: {ADMIN_USERNAME}")
