"""
🎓 SI STUDENT ACCOUNT - ডাটাবেস সংযোগ এবং ম্যানেজমেন্ট
database/db.py

SQLite ডাটাবেস সংযোগ এবং ক্রিয়াকলাপ পরিচালনা করে
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
import logging

# লগিং সেটাপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """SQLite ডাটাবেস ম্যানেজার ক্লাস"""
    
    def __init__(self, db_path='data/database.db'):
        """
        ডাটাবেস ইনিশিয়ালাইজ করুন
        
        Args:
            db_path (str): ডাটাবেস ফাইলের পাথ
        """
        self.db_path = db_path
        self.connection = None
        
        # ডাটা ডিরেক্টরি তৈরি করুন যদি না থাকে
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        logger.info(f"Database initialized at: {db_path}")
    
    def connect(self):
        """ডাটাবেসের সাথে সংযোগ স্থাপন করুন"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info("Database connection established")
            return self.connection
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def disconnect(self):
        """ডাটাবেস সংযোগ বন্ধ করুন"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    @contextmanager
    def get_cursor(self):
        """
        কন্টেক্সট ম্যানেজার দিয়ে কার্সর পান
        
        Usage:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT * FROM student")
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()
    
    def initialize_schema(self, schema_path='database/schema.sql'):
        """
        ডাটাবেস স্কিমা ইনিশিয়ালাইজ করুন
        
        Args:
            schema_path (str): schema.sql ফাইলের পাথ
        """
        if not os.path.exists(schema_path):
            logger.error(f"Schema file not found: {schema_path}")
            return False
        
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.executescript(schema_sql)
            self.connection.commit()
            
            logger.info("Database schema initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing schema: {e}")
            return False
    
    def create_admin(self, username, password_hash, email, full_name, phone=None):
        """
        নতুন এডমিন তৈরি করুন
        
        Args:
            username (str): এডমিন ইউজারনেম
            password_hash (str): পাসওয়ার্ড হ্যাশ
            email (str): ইমেইল
            full_name (str): সম্পূর্ণ নাম
            phone (str): ফোন নম্বর
        
        Returns:
            bool: সফল হলে True
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO admin 
                    (username, password_hash, email, full_name, phone, role, status)
                    VALUES (?, ?, ?, ?, ?, 'admin', 'active')
                """, (username, password_hash, email, full_name, phone))
                logger.info(f"Admin created: {username}")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"Admin already exists: {username}")
            return False
        except Exception as e:
            logger.error(f"Error creating admin: {e}")
            return False
    
    def get_admin(self, username):
        """
        ইউজারনেম দিয়ে এডমিন খুঁজুন
        
        Args:
            username (str): এডমিন ইউজারনেম
        
        Returns:
            dict: এডমিন ডাটা অথবা None
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching admin: {e}")
            return None
    
    def create_student(self, telegram_id, username, password_hash, student_email, 
                      email_domain, first_name, last_name, university_name, student_id, **kwargs):
        """
        নতুন স্টুডেন্ট তৈরি করুন
        
        Args:
            telegram_id (str): টেলিগ্রাম আইডি
            username (str): ইউজারনেম
            password_hash (str): পাসওয়ার্ড হ্যাশ
            student_email (str): শিক্ষা প্রতিষ্ঠানের ইমেইল
            email_domain (str): ইমেইল ডোমেইন (.edu, .ac.bd ইত্যাদি)
            first_name (str): প্রথম নাম
            last_name (str): শেষ নাম
            university_name (str): বিশ্ববিদ্যালয়ের নাম
            student_id (str): ছাত্র আইডি
            **kwargs: অন্যান্য ঐচ্ছিক ফিল্ড
        
        Returns:
            int: নতুন স্টুডেন্টের ID অথবা None
        """
        try:
            full_name = f"{first_name} {kwargs.get('last_name', '')}"
            
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO student 
                    (telegram_id, username, password_hash, student_email, email_domain,
                     first_name, last_name, full_name, university_name, student_id,
                     middle_name, gender, date_of_birth, nationality, country,
                     phone, personal_email, account_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                """, (
                    telegram_id, username, password_hash, student_email, email_domain,
                    first_name, last_name, full_name, university_name, student_id,
                    kwargs.get('middle_name'),
                    kwargs.get('gender'),
                    kwargs.get('date_of_birth'),
                    kwargs.get('nationality'),
                    kwargs.get('country'),
                    kwargs.get('phone'),
                    kwargs.get('personal_email')
                ))
                
                student_id_db = cursor.lastrowid
                logger.info(f"Student created: {username} (ID: {student_id_db})")
                return student_id_db
        except sqlite3.IntegrityError:
            logger.warning(f"Student already exists: {student_email}")
            return None
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            return None
    
    def get_student(self, student_email=None, username=None, telegram_id=None):
        """
        স্টুডেন্ট খুঁজুন
        
        Args:
            student_email (str): ইমেইল
            username (str): ইউজারনেম
            telegram_id (str): টেলিগ্রাম আইডি
        
        Returns:
            dict: স্টুডেন্ট ডাটা অথবা None
        """
        try:
            with self.get_cursor() as cursor:
                if student_email:
                    cursor.execute("SELECT * FROM student WHERE student_email = ?", (student_email,))
                elif username:
                    cursor.execute("SELECT * FROM student WHERE username = ?", (username,))
                elif telegram_id:
                    cursor.execute("SELECT * FROM student WHERE telegram_id = ?", (telegram_id,))
                else:
                    return None
                
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error fetching student: {e}")
            return None
    
    def add_credit(self, student_id, amount, transaction_type, description="", admin_id=None):
        """
        স্টুডেন্টের ক্রেডিট যোগ করুন
        
        Args:
            student_id (int): স্টুডেন্ট আইডি
            amount (float): ক্রেডিট পরিমাণ
            transaction_type (str): লেনদেন টাইপ
            description (str): বর্ণনা
            admin_id (int): এডমিন আইডি (ঐচ্ছিক)
        
        Returns:
            bool: সফল হলে True
        """
        try:
            with self.get_cursor() as cursor:
                # বর্তমান ব্যালেন্স পান
                cursor.execute("SELECT credit_balance FROM student WHERE id = ?", (student_id,))
                result = cursor.fetchone()
                
                if not result:
                    logger.warning(f"Student not found: {student_id}")
                    return False
                
                current_balance = float(result['credit_balance'])
                new_balance = current_balance + amount
                
                # স্টুডেন্ট ব্যালেন্স আপডেট করুন
                cursor.execute(
                    "UPDATE student SET credit_balance = ? WHERE id = ?",
                    (new_balance, student_id)
                )
                
                # লেনদেন রেকর্ড করুন
                cursor.execute("""
                    INSERT INTO credit_transaction
                    (student_id, transaction_type, amount, description, balance_after, admin_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'completed')
                """, (student_id, transaction_type, amount, description, new_balance, admin_id))
                
                logger.info(f"Credit added - Student: {student_id}, Amount: {amount}")
                return True
        except Exception as e:
            logger.error(f"Error adding credit: {e}")
            return False
    
    def deduct_credit(self, student_id, amount, transaction_type, description=""):
        """
        স্টুডেন্টের ক্রেডিট কাটুন
        
        Args:
            student_id (int): স্টুডেন্ট আইডি
            amount (float): ক্রেডিট পরিমাণ
            transaction_type (str): লেনদেন টাইপ
            description (str): বর্ণনা
        
        Returns:
            bool: সফল হলে True
        """
        try:
            with self.get_cursor() as cursor:
                # বর্তমান ব্যালেন্স পান
                cursor.execute("SELECT credit_balance FROM student WHERE id = ?", (student_id,))
                result = cursor.fetchone()
                
                if not result:
                    logger.warning(f"Student not found: {student_id}")
                    return False
                
                current_balance = float(result['credit_balance'])
                
                if current_balance < amount:
                    logger.warning(f"Insufficient credit - Student: {student_id}")
                    return False
                
                new_balance = current_balance - amount
                
                # স্টুডেন্ট ব্যালেন্স আপডেট করুন
                cursor.execute(
                    "UPDATE student SET credit_balance = ? WHERE id = ?",
                    (new_balance, student_id)
                )
                
                # লেনদেন রেকর্ড করুন
                cursor.execute("""
                    INSERT INTO credit_transaction
                    (student_id, transaction_type, amount, description, balance_after, status)
                    VALUES (?, ?, ?, ?, ?, 'completed')
                """, (student_id, transaction_type, amount, description, new_balance))
                
                logger.info(f"Credit deducted - Student: {student_id}, Amount: {amount}")
                return True
        except Exception as e:
            logger.error(f"Error deducting credit: {e}")
            return False


# গ্লোবাল ডাটাবেস ইনস্ট্যান্স
db = Database()


if __name__ == "__main__":
    # ডাটাবেস সেটআপ টেস্ট
    print("🎓 SI STUDENT ACCOUNT - ডাটাবেস সেটআপ")
    print("=" * 50)
    
    # ডাটাবেস ইনিশিয়ালাইজ করুন
    db.connect()
    if db.initialize_schema():
        print("✅ ডাটাবেস স্কিমা সফলভাবে তৈরি হয়েছে")
    else:
        print("❌ ডাটাবেস স্কিমা তৈরিতে ত্রুটি")
    
    db.disconnect()
