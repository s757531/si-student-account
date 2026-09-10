"""
🎓 SI STUDENT ACCOUNT - ভ্যালিডেশন ফাংশন
utils/validators.py

ইমেইল, ফোন নম্বর এবং অন্যান্য তথ্য যাচাই করুন
"""

import re
from email_validator import validate_email, EmailNotValidError


def validate_student_email(email, allowed_domains):
    """
    শিক্ষা প্রতিষ্ঠানের ইমেইল যাচাই করুন
    
    Args:
        email (str): ইমেইল ঠিকানা
        allowed_domains (list): অনুমতিপ্রাপ্ত ডোমেইন
    
    Returns:
        tuple: (valid, message)
    """
    try:
        # ইমেইল ফরম্যাট যাচাই করুন
        valid = validate_email(email)
        email = valid.email
        
        # ডোমেইন চেক করুন
        domain = email.split('@')[1]
        
        # শিক্ষা ডোমেইন চেক করুন
        has_edu_domain = any(domain.endswith(allowed) for allowed in allowed_domains)
        
        if not has_edu_domain:
            return False, f"❌ শিক্ষা প্রতিষ্ঠানের ইমেইল ব্যবহার করুন ({', '.join(allowed_domains)})"
        
        return True, "✅ ইমেইল সঠিক"
    except EmailNotValidError as e:
        return False, f"❌ অবৈধ ইমেইল: {str(e)}"
    except Exception as e:
        return False, f"❌ ত্রুটি: {str(e)}"


def validate_phone(phone):
    """
    ফোন নম্বর যাচাই করুন
    
    Args:
        phone (str): ফোন নম্বর
    
    Returns:
        tuple: (valid, message)
    """
    # ফোন নম্বর প্যাটার্ন (সাধারণ)
    pattern = r'^[\d\s\-\+()]+$'
    
    if not phone:
        return False, "❌ ফোন নম্বর প্রয়োজন"
    
    if len(phone) < 10:
        return False, "❌ ফোন নম্বর কমপক্ষে ১০ অঙ্ক হতে হবে"
    
    if not re.match(pattern, phone):
        return False, "❌ অবৈধ ফোন নম্বর ফরম্যাট"
    
    return True, "✅ ফোন নম্বর সঠিক"


def validate_password(password):
    """
    পাসওয়ার্ড যাচাই করুন
    
    Args:
        password (str): পাসওয়ার্ড
    
    Returns:
        tuple: (valid, message)
    """
    if not password:
        return False, "❌ পাসওয়ার্ড প্রয়োজন"
    
    if len(password) < 8:
        return False, "❌ পাসওয়ার্ড কমপক্ষে ৮ অক্ষর হতে হবে"
    
    # অন্তত একটি বড় অক্ষর চেক করুন
    if not re.search(r'[A-Z]', password):
        return False, "❌ পাসওয়ার্ডে অন্তত একটি বড় অক্ষর থাকতে হবে"
    
    # অন্তত একটি ছোট অক্ষর চেক করুন
    if not re.search(r'[a-z]', password):
        return False, "❌ পাসওয়ার্ডে অন্তত একটি ছোট অক্ষর থাকতে হবে"
    
    # অন্তত একটি সংখ্যা চেক করুন
    if not re.search(r'\d', password):
        return False, "❌ পাসওয়ার্ডে অন্তত একটি সংখ্যা থাকতে হবে"
    
    return True, "✅ পাসওয়ার্ড শক্তিশালী"


def validate_username(username):
    """
    ইউজারনেম যাচাই করুন
    
    Args:
        username (str): ইউজারনেম
    
    Returns:
        tuple: (valid, message)
    """
    if not username:
        return False, "❌ ইউজারনেম প্রয়োজন"
    
    if len(username) < 4:
        return False, "❌ ইউজারনেম কমপক্ষে ৪ অক্ষর হতে হবে"
    
    if len(username) > 20:
        return False, "❌ ইউজারনেম সর্বোচ্চ ২০ অক্ষর হতে পারে"
    
    # শুধুমাত্র অক্ষর, সংখ্যা এবং আন্ডারস্কোর অনুমতি
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "❌ ইউজারনেমে শুধুমাত্র অক্ষর, সংখ্যা এবং আন্ডারস্কোর ব্যবহার করুন"
    
    return True, "✅ ইউজারনেম সঠিক"
