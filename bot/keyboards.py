"""
🎓 SI STUDENT ACCOUNT - টেলিগ্রাম বট কীবোর্ড UI
bot/keyboards.py

টেলিগ্রাম বটের জন্য সমস্ত কাস্টম কীবোর্ড এবং বাটন সংজ্ঞায়িত করুন
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


class StudentKeyboards:
    """স্টুডেন্ট কীবোর্ড"""
    
    @staticmethod
    def main_menu():
        """মেইন মেনু কীবোর্ড"""
        keyboard = [
            [KeyboardButton("📝 রেজিস্ট্রেশন"), KeyboardButton("🔐 লগইন")],
            [KeyboardButton("💰 ক্রেডিট লোড"), KeyboardButton("📊 ব্যালেন্স দেখুন")],
            [KeyboardButton("📧 ইনবক্স"), KeyboardButton("🎯 কাজ সমূহ")],
            [KeyboardButton("⚙️ সেটিংস"), KeyboardButton("ℹ️ সাহায্য")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    @staticmethod
    def registration_menu():
        """রেজিস্ট্রেশন স্টেপ কীবোর্ড"""
        keyboard = [
            [KeyboardButton("🇺🇸 যুক্তরাষ্ট্র"), KeyboardButton("🇧🇩 বাংলাদেশ")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def gender_menu():
        """জেন্ডার নির্বাচন কীবোর্ড"""
        keyboard = [
            [KeyboardButton("👨 পুরুষ"), KeyboardButton("👩 নারী"), KeyboardButton("⚧️ অন্যান্য")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def degree_menu():
        """ডিগ্রি নির্বাচন কীবোর্ড"""
        keyboard = [
            [KeyboardButton("🎓 Bachelor's"), KeyboardButton("🎓 Master's")],
            [KeyboardButton("📜 Diploma"), KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def semester_menu():
        """সেমিস্টার নির্বাচন কীবোর্ড"""
        keyboard = [
            [KeyboardButton("🍂 Fall"), KeyboardButton("🌸 Spring")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def authenticated_menu():
        """প্রমাণীকৃত স্টুডেন্ট মেনু"""
        keyboard = [
            [KeyboardButton("💰 ক্রেডিট লোড"), KeyboardButton("📊 ব্যালেন্স")],
            [KeyboardButton("📧 ইনবক্স"), KeyboardButton("🎯 কাজ সমূহ")],
            [KeyboardButton("👤 প্রোফাইল"), KeyboardButton("⚙️ সেটিংস")],
            [KeyboardButton("🚪 লগআউট")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def inbox_menu():
        """ইনবক্স মেনু"""
        keyboard = [
            [KeyboardButton("📬 সব মেইল"), KeyboardButton("⭐ গুরুত্বপূর্ণ")],
            [KeyboardButton("🆕 নতুন"), KeyboardButton("🗑️ স্প্যাম")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def work_menu():
        """কাজ সমূহ মেনু"""
        keyboard = [
            [KeyboardButton("📋 পেন্ডিং"), KeyboardButton("⏳ চলমান")],
            [KeyboardButton("✅ সম্পন্ন"), KeyboardButton("❌ বাতিল")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def confirm_menu():
        """নিশ্চিতকরণ মেনু"""
        keyboard = [
            [KeyboardButton("✅ হ্যাঁ"), KeyboardButton("❌ না")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def settings_menu():
        """সেটিংস মেনু"""
        keyboard = [
            [KeyboardButton("🔐 পাসওয়ার্ড পরিবর্তন"), KeyboardButton("📧 ইমেইল আপডেট")],
            [KeyboardButton("📞 ফোন আপডেট"), KeyboardButton("🗑️ অ্যাকাউন্ট মুছুন")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def remove_keyboard():
        """কীবোর্ড সরান"""
        from telegram import ReplyKeyboardRemove
        return ReplyKeyboardRemove()


class AdminKeyboards:
    """এডমিন কীবোর্ড"""
    
    @staticmethod
    def admin_main_menu():
        """এডমিন মেইন মেনু"""
        keyboard = [
            [KeyboardButton("👥 স্টুডেন্ট ম্যানেজমেন্ট"), KeyboardButton("💰 ক্রেডিট ম্যানেজমেন্ট")],
            [KeyboardButton("📊 রিপোর্ট"), KeyboardButton("⚙️ সিস্টেম সেটিংস")],
            [KeyboardButton("📧 অ্যানাউন্সমেন্ট"), KeyboardButton("🚪 লগআউট")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def student_action_menu():
        """স্টুডেন্ট অ্যাকশন মেনু"""
        keyboard = [
            [KeyboardButton("📋 তালিকা দেখুন"), KeyboardButton("🔍 অনুসন্ধান")],
            [KeyboardButton("✏️ এডিট"), KeyboardButton("🚫 সাসপেন্ড")],
            [KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def credit_action_menu():
        """ক্রেডিট অ্যাকশন মেনু"""
        keyboard = [
            [KeyboardButton("➕ যোগ করুন"), KeyboardButton("➖ কাটুন")],
            [KeyboardButton("📊 ইতিহাস"), KeyboardButton("⬅️ ফিরে যান")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


class InlineKeyboards:
    """ইনলাইন কীবোর্ড (বাটন কোয়েরি এর জন্য)"""
    
    @staticmethod
    def confirmation_buttons():
        """নিশ্চিতকরণ ইনলাইন বাটন"""
        keyboard = [
            [InlineKeyboardButton("✅ হ্যাঁ", callback_data="confirm_yes")],
            [InlineKeyboardButton("❌ না", callback_data="confirm_no")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def student_details_buttons(student_id):
        """স্টুডেন্ট বিস্তারিত বাটন"""
        keyboard = [
            [InlineKeyboardButton("✏️ এডিট", callback_data=f"edit_student_{student_id}")],
            [InlineKeyboardButton("💰 ক্রেডিট সমন্বয়", callback_data=f"adjust_credit_{student_id}")],
            [InlineKeyboardButton("🚫 সাসপেন্ড", callback_data=f"suspend_student_{student_id}")],
            [InlineKeyboardButton("🔄 রিসেট", callback_data=f"reset_student_{student_id}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def pagination_buttons(page, total_pages, callback_prefix):
        """পেজিনেশন বাটন"""
        keyboard = []
        
        # পূর্ববর্তী বাটন
        if page > 1:
            keyboard.append(InlineKeyboardButton("⬅️ পূর্ববর্তী", callback_data=f"{callback_prefix}_prev_{page-1}"))
        
        # পৃষ্ঠা নম্বর
        keyboard.append(InlineKeyboardButton(f"📄 {page}/{total_pages}", callback_data="noop"))
        
        # পরবর্তী বাটন
        if page < total_pages:
            keyboard.append(InlineKeyboardButton("পরবর্তী ➡️", callback_data=f"{callback_prefix}_next_{page+1}"))
        
        return InlineKeyboardMarkup([keyboard])
    
    @staticmethod
    def email_action_buttons(email_id):
        """ইমেইল অ্যাকশন বাটন"""
        keyboard = [
            [InlineKeyboardButton("👁️ পড়া হয়েছে", callback_data=f"mark_read_{email_id}")],
            [InlineKeyboardButton("⭐ তারকা", callback_data=f"star_email_{email_id}")],
            [InlineKeyboardButton("🗑️ ডিলিট", callback_data=f"delete_email_{email_id}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def work_status_buttons(work_id):
        """কাজের স্ট্যাটাস বাটন"""
        keyboard = [
            [InlineKeyboardButton("⏳ চলমান", callback_data=f"work_status_{work_id}_in_progress")],
            [InlineKeyboardButton("✅ সম্পন্ন", callback_data=f"work_status_{work_id}_completed")],
            [InlineKeyboardButton("❌ বাতিল", callback_data=f"work_status_{work_id}_cancelled")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def credit_load_amount_buttons():
        """ক্রেডিট লোড পরিমাণ বাটন"""
        keyboard = [
            [InlineKeyboardButton("$5", callback_data="load_credit_5")],
            [InlineKeyboardButton("$10", callback_data="load_credit_10")],
            [InlineKeyboardButton("$20", callback_data="load_credit_20")],
            [InlineKeyboardButton("$50", callback_data="load_credit_50")],
            [InlineKeyboardButton("💳 কাস্টম", callback_data="load_credit_custom")]
        ]
        return InlineKeyboardMarkup(keyboard)
