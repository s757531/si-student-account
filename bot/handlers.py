"""
🎓 SI STUDENT ACCOUNT - টেলিগ্রাম বট হ্যান্ডেলার
bot/handlers.py

সমস্ত টেলিগ্রাম কমান্ড এবং মেসেজ হ্যান্ডলার
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import logging
from datetime import datetime
from .keyboards import StudentKeyboards, AdminKeyboards, InlineKeyboards
from config.settings import EDUCATIONAL_DOMAINS
from database.db import db
from utils.validators import (
    validate_student_email, validate_phone, validate_password, validate_username
)
from utils.email_domain import get_domain_country, is_educational_email
from utils.security import hash_password, verify_password

logger = logging.getLogger(__name__)

# কথোপকথন স্টেট
REGISTRATION_COUNTRY = 1
REGISTRATION_EMAIL = 2
REGISTRATION_PASSWORD = 3
REGISTRATION_CONFIRM_PASSWORD = 4
REGISTRATION_FIRST_NAME = 5
REGISTRATION_LAST_NAME = 6
REGISTRATION_PHONE = 7
REGISTRATION_GENDER = 8
REGISTRATION_UNIVERSITY = 9
REGISTRATION_STUDENT_ID = 10
REGISTRATION_DEGREE = 11
REGISTRATION_CONFIRM = 12

LOGIN_EMAIL = 20
LOGIN_PASSWORD = 21


class StudentHandlers:
    """স্টুডেন্ট হ্যান্ডেলার"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /start কমান্ড হ্যান্ডেলার
        """
        user = update.effective_user
        
        welcome_text = f"""
🎓 স্বাগতম {user.first_name}!

SI STUDENT ACCOUNT এ আপনাকে স্বাগতম। এটি একটি সম্পূর্ণ স্টুডেন্ট ম্যানেজমেন্ট সিস্টেম।

🇺🇸 যুক্তরাষ্ট্র এবং 🇧🇩 বাংলাদেশের জন্য উপলব্ধ।

আপনি যা করতে পারেন:
✅ রেজিস্ট্রেশন করুন
✅ লগইন করুন
✅ ক্রেডিট লোড করুন
✅ ইনবক্স ম্যানেজ করুন
✅ কাজ ট্র্যাক করুন

শুরু করতে নিম্নোক্ত অপশন থেকে বেছে নিন:
        """
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=StudentKeyboards.main_menu()
        )
    
    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /help কমান্ড হ্যান্ডেলার
        """
        help_text = """
📚 সাহায্য এবং গাইড

**কমান্ড সমূহ:**
/start - বট শুরু করুন
/help - এই সাহায্য পান
/register - নতুন অ্যাকাউন্ট তৈরি করুন
/login - লগইন করুন
/logout - লগআউট করুন
/profile - আপনার প্রোফাইল দেখুন
/balance - ক্রেডিট ব্যালেন্স দেখুন
/inbox - ইনবক্স খুলুন
/works - সকল কাজ দেখুন
/settings - সেটিংস পরিবর্তন করুন

**কাজ করার ধাপসমূহ:**
1. রেজিস্ট্রেশন করুন
2. ইমেইল ভেরিফাই করুন
3. ক্রেডিট লোড করুন
4. কাজ শুরু করুন

**প্রশ্ন থাকলে:**
 আমাদের সাথে যোগাযোগ করুন: admin@siaccount.edu
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    @staticmethod
    async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        রেজিস্ট্রেশন শুরু করুন
        """
        text = """
🎓 নতুন অ্যাকাউন্ট তৈরি করুন

প্রথমে আপনার দেশ নির্বাচন করুন:
        """
        
        await update.message.reply_text(
            text,
            reply_markup=StudentKeyboards.registration_menu()
        )
        return REGISTRATION_COUNTRY
    
    @staticmethod
    async def registration_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        দেশ নির্বাচন
        """
        country = update.message.text
        
        if country == "🇺🇸 যুক্তরাষ্ট্র":
            context.user_data['country'] = 'USA'
            allowed_domains = ['.edu']
        elif country == "🇧🇩 বাংলাদেশ":
            context.user_data['country'] = 'Bangladesh'
            allowed_domains = ['.ac.bd', '.edu.bd']
        else:
            await update.message.reply_text(
                "❌ অবৈধ নির্বাচন। আবার চেষ্টা করুন।",
                reply_markup=StudentKeyboards.registration_menu()
            )
            return REGISTRATION_COUNTRY
        
        context.user_data['allowed_domains'] = allowed_domains
        
        text = f"""
 আপনার শিক্ষা প্রতিষ্ঠানের ইমেইল দিন।

✅ অনুমোদিত ডোমেইনস: {', '.join(allowed_domains)}

উদাহরণ: student@university.edu
        """
        
        await update.message.reply_text(text)
        return REGISTRATION_EMAIL
    
    @staticmethod
    async def registration_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        শিক্ষা ইমেইল যাচাইকরণ
        """
        email = update.message.text.strip().lower()
        allowed_domains = context.user_data.get('allowed_domains', [])
        
        # ইমেইল ভ্যালিডেশন
        valid, message = validate_student_email(email, allowed_domains)
        
        if not valid:
            await update.message.reply_text(
                f"❌ {message}\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_EMAIL
        
        # ডাটাবেসে ইমেইল চেক করুন
        existing_student = db.get_student(student_email=email)
        if existing_student:
            await update.message.reply_text(
                "❌ এই ইমেইল ইতিমধ্যে ব্যবহৃত হয়েছে।\n\nআলাদা ইমেইল চেষ্টা করুন:"
            )
            return REGISTRATION_EMAIL
        
        context.user_data['email'] = email
        domain, country = get_domain_country(email)
        context.user_data['email_domain'] = domain
        
        await update.message.reply_text(
            f"✅ ইমেইল গৃহীত: {email}\n\nএখন একটি শক্তিশালী পাসওয়ার্ড দিন:\n\n" +
            "প্রয়োজনীয়তা:\n" +
            "• কমপক্ষে ৮ অক্ষর\n" +
            "• কমপক্ষে একটি বড় অক্ষর (A-Z)\n" +
            "• কমপক্ষে একটি ছোট অক্ষর (a-z)\n" +
            "• কমপক্ষে একটি সংখ্যা (0-9)"
        )
        return REGISTRATION_PASSWORD
    
    @staticmethod
    async def registration_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        পাসওয়ার্ড যাচাইকরণ
        """
        password = update.message.text
        
        # পাসওয়ার্ড ভ্যালিডেশন
        valid, message = validate_password(password)
        
        if not valid:
            await update.message.reply_text(
                f"❌ {message}\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_PASSWORD
        
        context.user_data['password'] = password
        
        await update.message.reply_text(
            "✅ পাসওয়ার্ড গৃহীত।\n\nপাসওয়ার্ড নিশ্চিত করুন (আবার দিন):"
        )
        return REGISTRATION_CONFIRM_PASSWORD
    
    @staticmethod
    async def registration_confirm_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        পাসওয়ার্ড নিশ্চিতকরণ
        """
        confirm_password = update.message.text
        original_password = context.user_data.get('password')
        
        if confirm_password != original_password:
            await update.message.reply_text(
                "❌ পাসওয়ার্ড মিলে না।\n\nআবার দিন:"
            )
            return REGISTRATION_CONFIRM_PASSWORD
        
        context.user_data['password_confirmed'] = True
        
        await update.message.reply_text(
            "✅ পাসওয়ার্ড সংরক্ষিত।\n\nআপনার প্রথম নাম দিন:"
        )
        return REGISTRATION_FIRST_NAME
    
    @staticmethod
    async def registration_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        প্রথম নাম ইনপুট
        """
        first_name = update.message.text.strip()
        
        if len(first_name) < 2:
            await update.message.reply_text(
                "❌ নাম কমপক্ষে ২ অক্ষর হতে হবে।\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_FIRST_NAME
        
        context.user_data['first_name'] = first_name
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার শেষ নাম দিন:"
        )
        return REGISTRATION_LAST_NAME
    
    @staticmethod
    async def registration_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        শেষ নাম ইনপুট
        """
        last_name = update.message.text.strip()
        
        if len(last_name) < 2:
            await update.message.reply_text(
                "❌ নাম কমপক্ষে ২ অক্ষর হতে হবে।\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_LAST_NAME
        
        context.user_data['last_name'] = last_name
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার ফোন নম্বর দিন (ঐচ্ছিক - এড়িয়ে যেতে 'না' লিখুন):"
        )
        return REGISTRATION_PHONE
    
    @staticmethod
    async def registration_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        ফোন নম্বর ইনপুট
        """
        phone = update.message.text.strip()
        
        if phone.lower() == 'না':
            context.user_data['phone'] = None
        else:
            valid, message = validate_phone(phone)
            if not valid:
                await update.message.reply_text(
                    f"❌ {message}\n\nআবার চেষ্টা করুন:"
                )
                return REGISTRATION_PHONE
            context.user_data['phone'] = phone
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার বিশ্ববিদ্যালয়ের নাম দিন:"
        )
        return REGISTRATION_UNIVERSITY
    
    @staticmethod
    async def registration_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        বিশ্ববিদ্যালয় নাম ইনপুট
        """
        university = update.message.text.strip()
        
        if len(university) < 3:
            await update.message.reply_text(
                "❌ বিশ্ববিদ্যালয়ের নাম কমপক্ষে ৩ অক্ষর হতে হবে।\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_UNIVERSITY
        
        context.user_data['university'] = university
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার শিক্ষার্থী আইডি দিন:"
        )
        return REGISTRATION_STUDENT_ID
    
    @staticmethod
    async def registration_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        শিক্ষার্থী আইডি ইনপুট
        """
        student_id = update.message.text.strip()
        
        if len(student_id) < 3:
            await update.message.reply_text(
                "❌ শিক্ষার্থী আইডি কমপক্ষে ৩ অক্ষর হতে হবে।\n\nআবার চেষ্টা করুন:"
            )
            return REGISTRATION_STUDENT_ID
        
        context.user_data['student_id'] = student_id
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার ডিগ্রি নির্বাচন করুন:",
            reply_markup=StudentKeyboards.degree_menu()
        )
        return REGISTRATION_DEGREE
    
    @staticmethod
    async def registration_degree(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        ডিগ্রি নির্বাচন
        """
        degree = update.message.text.strip()
        
        if degree not in ["🎓 Bachelor's", "🎓 Master's", "📜 Diploma"]:
            await update.message.reply_text(
                "❌ অবৈধ নির্বাচন।\n\nআবার চেষ্টা করুন:",
                reply_markup=StudentKeyboards.degree_menu()
            )
            return REGISTRATION_DEGREE
        
        context.user_data['degree'] = degree.replace('🎓 ', '').replace('📜 ', '')
        
        await update.message.reply_text(
            "✅ গৃহীত।\n\nআপনার জেন্ডার নির্বাচন করুন:",
            reply_markup=StudentKeyboards.gender_menu()
        )
        return REGISTRATION_GENDER
    
    @staticmethod
    async def registration_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        জেন্ডার নির্বাচন
        """
        gender = update.message.text.strip()
        
        gender_map = {
            '👨 পুরুষ': 'Male',
            '👩 নারী': 'Female',
            '⚧️ অন্যান্য': 'Other'
        }
        
        if gender not in gender_map:
            await update.message.reply_text(
                "❌ অবৈধ নির্বাচন।\n\nআবার চেষ্টা করুন:",
                reply_markup=StudentKeyboards.gender_menu()
            )
            return REGISTRATION_GENDER
        
        context.user_data['gender'] = gender_map[gender]
        
        # সারাংশ দেখান
        summary = f"""
📋 রেজিস্ট্রেশন সারাংশ

🇺🇸/🇧🇩 দেশ: {context.user_data.get('country')}
📧 ইমেইল: {context.user_data.get('email')}
👤 নাম: {context.user_data.get('first_name')} {context.user_data.get('last_name')}
📞 ফোন: {context.user_data.get('phone') or 'প্রদান করা হয়নি'}
🎓 বিশ্ববিদ্যালয়: {context.user_data.get('university')}
🆔 শিক্ষার্থী আইডি: {context.user_data.get('student_id')}
📜 ডিগ্রি: {context.user_data.get('degree')}
👥 জেন্ডার: {context.user_data.get('gender')}

✅ সবকিছু ঠিক আছে?
        """
        
        await update.message.reply_text(
            summary,
            reply_markup=StudentKeyboards.confirm_menu()
        )
        return REGISTRATION_CONFIRM
    
    @staticmethod
    async def registration_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        রেজিস্ট্রেশন নিশ্চিতকরণ
        """
        choice = update.message.text.strip()
        
        if choice == "✅ হ্যাঁ":
            # ডাটাবেসে যোগ করুন
            try:
                # ইউজারনেম তৈরি করুন
                first_name = context.user_data.get('first_name')
                email = context.user_data.get('email')
                username = f"{first_name.lower()}{email.split('@')[0].split('.')[0]}"
                
                # ইউজারনেম ভ্যালিডেশন
                valid, message = validate_username(username)
                if not valid:
                    username = f"{first_name.lower()}_{update.effective_user.id}"
                
                # পাসওয়ার্ড হ্যাশ করুন
                password_hash = hash_password(context.user_data.get('password'))
                
                # ডাটাবেসে স্টুডেন্ট যোগ করুন
                student_id = db.create_student(
                    telegram_id=str(update.effective_user.id),
                    username=username,
                    password_hash=password_hash,
                    student_email=email,
                    email_domain=context.user_data.get('email_domain'),
                    first_name=context.user_data.get('first_name'),
                    last_name=context.user_data.get('last_name'),
                    university_name=context.user_data.get('university'),
                    student_id=context.user_data.get('student_id'),
                    phone=context.user_data.get('phone'),
                    gender=context.user_data.get('gender'),
                    country=context.user_data.get('country'),
                    nationality=context.user_data.get('country')
                )
                
                if student_id:
                    success_text = f"""
✅ রেজিস্ট্রেশন সফল!

🎉 আপনার অ্যাকাউন্ট তৈরি হয়েছে।

👤 ইউজারনেম: {username}
🆔 অ্যাকাউন্ট আইডি: {student_id}

📧 পরবর্তী ধাপ: আপনার ইমেইল ভেরিফাই করুন

আপনার ইনবক্সে একটি ভেরিফিকেশন লিঙ্ক পাবেন।
                    """
                    await update.message.reply_text(
                        success_text,
                        reply_markup=StudentKeyboards.main_menu()
                    )
                    context.user_data.clear()
                    return ConversationHandler.END
                else:
                    await update.message.reply_text(
                        "❌ রেজিস্ট্রেশনে সমস্যা হয়েছে।\n\nআবার চেষ্টা করুন।",
                        reply_markup=StudentKeyboards.main_menu()
                    )
                    context.user_data.clear()
                    return ConversationHandler.END
            
            except Exception as e:
                logger.error(f"Registration error: {e}")
                await update.message.reply_text(
                    f"❌ অপ্রত্যাশিত ত্রুটি: {str(e)}\n\nআবার চেষ্টা করুন।",
                    reply_markup=StudentKeyboards.main_menu()
                )
                context.user_data.clear()
                return ConversationHandler.END
        
        elif choice == "❌ না":
            await update.message.reply_text(
                "🔄 রেজিস্ট্রেশন বাতিল করা হয়েছে।\n\nশুরু থেকে শুরু করতে /register ব্যবহার করুন।",
                reply_markup=StudentKeyboards.main_menu()
            )
            context.user_data.clear()
            return ConversationHandler.END
        
        else:
            await update.message.reply_text(
                "❌ অবৈধ নির্বাচন।\n\nআবার চেষ্টা করুন:",
                reply_markup=StudentKeyboards.confirm_menu()
            )
            return REGISTRATION_CONFIRM
    
    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        কথোপকথন বাতিল করুন
        """
        await update.message.reply_text(
            "❌ কথোপকথন বাতিল করা হয়েছে।",
            reply_markup=StudentKeyboards.main_menu()
        )
        return ConversationHandler.END
