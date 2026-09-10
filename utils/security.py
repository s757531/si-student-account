"""
🎓 SI STUDENT ACCOUNT - নিরাপত্তা ফাংশন
utils/security.py

পাসওয়ার্ড এনক্রিপশন এবং নিরাপত্তা পরিচালনা করুন
"""

import hashlib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """
    পাসওয়ার্ড হ্যাশ করুন (werkzeug ব্যবহার করে)
    
    Args:
        password (str): প্লেইন টেক্সট পাসওয়ার্ড
    
    Returns:
        str: হ্যাশ করা পাসওয়ার্ড
    """
    return generate_password_hash(password, method='scrypt')


def verify_password(password, hash_password):
    """
    পাসওয়ার্ড যাচাই করুন
    
    Args:
        password (str): প্লেইন টেক্সট পাসওয়ার্ড
        hash_password (str): হ্যাশ করা পাসওয়ার্ড
    
    Returns:
        bool: সঠিক হলে True
    """
    return check_password_hash(hash_password, password)


def generate_token(length=32):
    """
    নিরাপদ টোকেন তৈরি করুন
    
    Args:
        length (int): টোকেনের দৈর্ঘ্য
    
    Returns:
        str: নিরাপদ হেক্স টোকেন
    """
    return secrets.token_hex(length)


def generate_otp(length=6):
    """
    OTP তৈরি করুন
    
    Args:
        length (int): OTP এর সংখ্যা
    
    Returns:
        str: সংখ্যাসূচক OTP
    """
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))
