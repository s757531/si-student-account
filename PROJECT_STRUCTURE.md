# 🎓 SI STUDENT ACCOUNT - প্রজেক্ট স্ট্রাকচার

## 📁 ফোল্ডার এবং ফাইলের বিন্যাস

```
si-student-account/
│
├── 📁 bot/                          # টেলিগ্রাম বট ফাইলস
│   ├── __init__.py
│   ├── main.py                      # বট এন্ট্রি পয়েন্ট
│   ├── handlers.py                  # টেলিগ্রাম হ্যান্ডেলার
│   └── keyboards.py                 # বট বাটন/কীবোর্ড
│
├── 📁 admin_panel/                  # এডমিন ড্যাশবোর্ড (Flask)
│   ├── __init__.py
│   ├── app.py                       # Flask এপ্লিকেশন
│   ├── auth.py                      # এডমিন লগইন
│   ├── routes.py                    # রুটস/পেজ
│   └── 📁 templates/                # HTML টেমপ্লেট
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── users.html
│       └── settings.html
│
├── 📁 database/                     # ডাটাবেস এবং মডেল
│   ├── __init__.py
│   ├── db.py                        # ডাটাবেস সংযোগ
│   ├── models.py                    # ডাটাবেস টেবিল মডেল
│   └── schema.sql                   # SQL স্কিমা
│
├── 📁 config/                       # কনফিগারেশন
│   ├── __init__.py
│   ├── settings.py                  # অ্যাপ সেটিংস
│   └── secrets.py                   # API কী এবং গোপন তথ্য
│
├── 📁 utils/                        # সহায়ক ফাংশন
│   ├── __init__.py
│   ├── validators.py                # ইমেইল, ফোন ভ্যালিডেশন
│   ├── email_domain.py              # শিক্ষা প্রতিষ্ঠান ইমেইল চেক
│   └── security.py                  # পাসওয়ার্ড এনক্রিপশন
│
├── 📁 data/                         # ডাটা ফাইলস
│   ├── database.db                  # SQLite ডাটাবেস (অটো জেনারেট)
│   └── logs.txt                     # লগ ফাইল
│
├── 📁 docs/                         # ডকুমেন্টেশন
│   ├── INSTALLATION.md              # ইনস্টলেশন গাইড
│   ├── API.md                       # API ডকুমেন্টেশন
│   └── DATABASE.md                  # ডাটাবেস গাইড
│
├── requirements.txt                 # Python ডিপেন্ডেন্সি
├── .env.example                     # পরিবেশ ভেরিয়েবল টেমপ্লেট
├── .gitignore                       # গিট ইগনোর ফাইল
├── README.md                        # প্রজেক্ট পরিচয়
└── run.py                           # মেইন এন্ট্রি পয়েন্ট

```

---

## 📚 ফাইলের বিবরণ

### **bot/main.py** - টেলিগ্রাম বট
- বট স্টার্ট করা
- মেসেজ হ্যান্ডলিং

### **admin_panel/app.py** - এডমিন ড্যাশবোর্ড
- Flask ওয়েব সার্ভার
- এডমিন ইউজার ম্যানেজমেন্ট

### **database/models.py** - ডাটাবেস মডেল
- Student (ছাত্র তথ্য)
- Admin (প্রশাসক)
- Credit (ক্রেডিট লেনদেন)
- Inbox (ইনবক্স মেইল)

### **config/settings.py** - সেটিংস
- টেলিগ্রাম API টোকেন
- ডাটাবেস পাথ
- ওয়েব সার্ভার পোর্ট

---

## 🎯 পরবর্তী ধাপ
**Phase 1.2:** ডাটাবেস স্কিমা এবং মডেল তৈরি
