-- 🎓 SI STUDENT ACCOUNT - ডাটাবেস স্কিমা
-- SQLite Database Schema

-- ========================================
-- 📌 ADMIN টেবিল
-- ========================================
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT DEFAULT 'admin',
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- ========================================
-- 👤 STUDENT টেবিল
-- ========================================
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    
    -- ইমেইল তথ্য
    student_email TEXT UNIQUE NOT NULL,
    email_domain TEXT NOT NULL,  -- .edu, .ac.bd, .edu.bd ইত্যাদি
    personal_email TEXT,
    
    -- ব্যক্তিগত তথ্য
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT,  -- Male, Female, Other
    date_of_birth DATE,
    nationality TEXT,
    country TEXT,
    
    -- যোগাযোগ তথ্য
    phone TEXT,
    alternate_phone TEXT,
    
    -- ঠিকানা
    address_country TEXT,
    address_state TEXT,
    address_city TEXT,
    address_postal_code TEXT,
    
    -- শিক্ষা তথ্য
    college_name TEXT,
    university_name TEXT NOT NULL,
    campus TEXT,
    department TEXT,
    program_course TEXT,
    degree TEXT,  -- Bachelor's, Master's, Diploma
    academic_year TEXT,
    semester TEXT,  -- Fall, Spring
    session TEXT,
    
    -- শিক্ষার্থী পরিচয়
    student_id TEXT NOT NULL,
    registration_no TEXT,
    roll_no TEXT,
    admission_no TEXT,
    
    -- অ্যাকাউন্ট স্ট্যাটাস
    account_status TEXT DEFAULT 'pending',  -- pending, active, suspended, inactive
    account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_graduation DATE,
    verified_at TIMESTAMP,
    
    -- ক্রেডিট তথ্য
    credit_balance DECIMAL(10, 2) DEFAULT 0.00,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- ========================================
-- 💰 CREDIT টেবিল - লেনদেন ইতিহাস
-- ========================================
CREATE TABLE IF NOT EXISTS credit_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,  -- 'credit_load', 'work_deduction', 'refund', 'admin_adjustment'
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    balance_after DECIMAL(10, 2),
    admin_id INTEGER,
    status TEXT DEFAULT 'completed',  -- 'pending', 'completed', 'failed'
    payment_method TEXT,  -- 'manual_transfer', 'admin_add', 'work_fee'
    reference_no TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES student(id),
    FOREIGN KEY(admin_id) REFERENCES admin(id)
);

-- ========================================
-- 📧 INBOX টেবিল - ইমেইল ইনবক্স
-- ========================================
CREATE TABLE IF NOT EXISTS inbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    email_from TEXT NOT NULL,
    email_subject TEXT NOT NULL,
    email_body TEXT,
    email_body_html TEXT,
    sender_name TEXT,
    is_read BOOLEAN DEFAULT 0,
    starred BOOLEAN DEFAULT 0,
    category TEXT DEFAULT 'inbox',  -- inbox, important, archive, spam
    attachment_count INTEGER DEFAULT 0,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES student(id)
);

-- ========================================
-- 📝 WORK/BOARD টেবিল - কাজ/বোর্ড
-- ========================================
CREATE TABLE IF NOT EXISTS work_board (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    priority TEXT DEFAULT 'medium',  -- low, medium, high
    status TEXT DEFAULT 'pending',  -- pending, in_progress, completed, cancelled
    credit_required DECIMAL(10, 2) DEFAULT 0.00,
    credit_deducted DECIMAL(10, 2) DEFAULT 0.00,
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES student(id)
);

-- ========================================
-- 🔐 SECURITY টেবিল - লগইন প্রচেষ্টা
-- ========================================
CREATE TABLE IF NOT EXISTS login_attempt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    telegram_id TEXT,
    attempt_type TEXT NOT NULL,  -- 'success', 'failed', 'invalid_email', 'invalid_password'
    ip_address TEXT,
    device_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES student(id)
);

-- ========================================
-- 📊 ANALYTICS টেবিল - ব্যবহার বিশ্লেষণ
-- ========================================
CREATE TABLE IF NOT EXISTS user_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    total_credits_loaded DECIMAL(10, 2) DEFAULT 0.00,
    total_credits_spent DECIMAL(10, 2) DEFAULT 0.00,
    total_works_completed INTEGER DEFAULT 0,
    total_works_pending INTEGER DEFAULT 0,
    total_emails_received INTEGER DEFAULT 0,
    last_activity TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES student(id)
);

-- ========================================
-- 🛠️ SYSTEM LOG টেবিল
-- ========================================
CREATE TABLE IF NOT EXISTS system_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    user_type TEXT,  -- 'student', 'admin', 'system'
    user_id INTEGER,
    details TEXT,
    ip_address TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 🏢 EDUCATIONAL DOMAINS টেবিল
-- ========================================
CREATE TABLE IF NOT EXISTS educational_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE NOT NULL,  -- .edu, .ac.bd, .edu.bd, .ac.uk, .edu.au
    country TEXT NOT NULL,  -- USA, Bangladesh, UK, Australia
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 📇 INDEXES - দ্রুত অনুসন্ধানের জন্য
-- ========================================
CREATE INDEX IF NOT EXISTS idx_student_email ON student(student_email);
CREATE INDEX IF NOT EXISTS idx_student_telegram ON student(telegram_id);
CREATE INDEX IF NOT EXISTS idx_student_status ON student(account_status);
CREATE INDEX IF NOT EXISTS idx_credit_student ON credit_transaction(student_id);
CREATE INDEX IF NOT EXISTS idx_inbox_student ON inbox(student_id);
CREATE INDEX IF NOT EXISTS idx_work_student ON work_board(student_id);
CREATE INDEX IF NOT EXISTS idx_admin_username ON admin(username);

-- ========================================
-- 🌱 DEFAULT DATA - প্রাথমিক ডেটা
-- ========================================

-- শিক্ষা প্রতিষ্ঠানের ডোমেইনস
INSERT OR IGNORE INTO educational_domains (domain, country, description) VALUES
('.edu', 'USA', 'United States Educational Institution'),
('.ac.bd', 'Bangladesh', 'Bangladesh Academic Institution'),
('.edu.bd', 'Bangladesh', 'Bangladesh Educational Institution'),
('.ac.uk', 'UK', 'United Kingdom Academic Institution'),
('.edu.au', 'Australia', 'Australia Educational Institution');

-- ডিফল্ট এডমিন (প্রথম সেটাপে পরিবর্তন করুন)
-- ইউজারনেম: admin | পাসওয়ার্ড: admin123 (হ্যাশ করা)
INSERT OR IGNORE INTO admin (username, password_hash, email, full_name, phone, role)
VALUES (
    'admin',
    'scrypt:32768:8:1$aBc123DEfGhIjKlM$xYzAbCdEfGhIjKlMnOpQrStUvWxYz1234567890',
    'admin@siaccount.edu',
    'System Administrator',
    '+1-800-000-0000',
    'super_admin'
);