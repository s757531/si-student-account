"""
🎓 SI STUDENT ACCOUNT - এডমিন লগইন এবং প্রমাণীকরণ
admin_panel/auth.py
"""

from functools import wraps
from flask import session, redirect, url_for, request
import logging

logger = logging.getLogger(__name__)


def require_login(f):
    """
    লগইন প্রয়োজন ডেকোরেটর
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def require_admin_role(f):
    """
    এডমিন রোল প্রয়োজন ডেকোরেটর
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        # রোল চেক করুন (ভবিষ্যতে বাস্তবায়ন করুন)
        return f(*args, **kwargs)
    return decorated_function


def check_admin_session():
    """
    এডমিন সেশন চেক করুন
    """
    return 'admin_id' in session and 'admin_username' in session


def get_admin_session():
    """
    এডমিন সেশন তথ্য পান
    """
    if check_admin_session():
        return {
            'admin_id': session.get('admin_id'),
            'admin_username': session.get('admin_username'),
            'admin_email': session.get('admin_email')
        }
    return None
