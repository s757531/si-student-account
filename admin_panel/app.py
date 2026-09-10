"""
🎓 SI STUDENT ACCOUNT - এডমিন প্যানেল এপ্লিকেশন
admin_panel/app.py

Flask ওয়েব সার্ভার এবং রুটস
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import logging
from datetime import datetime, timedelta
from config.settings import (
    FLASK_ENV, SECRET_KEY, SERVER_HOST, SERVER_PORT,
    ADMIN_USERNAME, ADMIN_PASSWORD, DATABASE_PATH
)
from database.db import db
from utils.security import verify_password, hash_password
import os

# Flask অ্যাপ তৈরি করুন
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

# কনফিগারেশন
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = FLASK_ENV == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def login_required(f):
    """
    লগইন প্রয়োজন ডেকোরেটর
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    """
    প্রতিটি রিকোয়েস্টের আগে ডাটাবেস সংযোগ চেক করুন
    """
    if not db.connection:
        db.connect()


@app.after_request
def after_request(response):
    """
    CORS হেডার যোগ করুন
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


@app.route('/')
def index():
    """
    ইন্ডেক্স পেজ - ড্যাশবোর্ডে রিডাইরেক্ট করুন
    """
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    এডমিন লগইন পেজ
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='ইউজারনেম এবং পাসওয়ার্ড প্রয়োজন'), 400
        
        # ডাটাবেসে এডমিন খুঁজুন
        admin = db.get_admin(username)
        
        if admin and verify_password(password, admin['password_hash']):
            # সেশনে এডমিন তথ্য সংরক্ষণ করুন
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            session['admin_email'] = admin['email']
            session.permanent = True
            
            logger.info(f"এডমিন লগইন সফল: {username}")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"এডমিন লগইন ব্যর্থ: {username}")
            return render_template('login.html', error='ভুল ইউজারনেম বা পাসওয়ার্ড'), 401
    
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    এডমিন লগআউট
    """
    session.clear()
    logger.info("এডমিন লগআউট")
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """
    এডমিন ড্যাশবোর্ড
    """
    try:
        # সিস্টেম স্ট্যাটিস্টিক্স পান
        with db.get_cursor() as cursor:
            # মোট স্টুডেন্ট
            cursor.execute("SELECT COUNT(*) as count FROM student")
            total_students = cursor.fetchone()['count']
            
            # সক্রিয় স্টুডেন্ট
            cursor.execute("SELECT COUNT(*) as count FROM student WHERE account_status = 'active'")
            active_students = cursor.fetchone()['count']
            
            # মোট ক্রেডিট লোডিং
            cursor.execute(
                "SELECT SUM(amount) as total FROM credit_transaction WHERE transaction_type = 'credit_load'"
            )
            result = cursor.fetchone()
            total_credit_loaded = result['total'] or 0.0
            
            # মোট কাজ
            cursor.execute("SELECT COUNT(*) as count FROM work_board")
            total_works = cursor.fetchone()['count']
            
            # সম্পন্ন কাজ
            cursor.execute("SELECT COUNT(*) as count FROM work_board WHERE status = 'completed'")
            completed_works = cursor.fetchone()['count']
        
        stats = {
            'total_students': total_students,
            'active_students': active_students,
            'total_credit_loaded': f"${total_credit_loaded:.2f}",
            'total_works': total_works,
            'completed_works': completed_works,
            'completion_rate': f"{(completed_works/total_works*100) if total_works > 0 else 0:.1f}%"
        }
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        logger.error(f"ড্যাশবোর্ড ত্রুটি: {e}")
        return render_template('dashboard.html', error='স্ট্যাটিস্টিক্স লোড করতে ব্যর্থ'), 500


@app.route('/api/students')
@login_required
def get_students():
    """
    সব স্টুডেন্ট তথ্য API
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    status_filter = request.args.get('status', '', type=str)
    
    try:
        with db.get_cursor() as cursor:
            # মোট সংখ্যা
            query = "SELECT COUNT(*) as count FROM student WHERE 1=1"
            params = []
            
            if search:
                query += " AND (student_email LIKE ? OR full_name LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])
            
            if status_filter:
                query += " AND account_status = ?"
                params.append(status_filter)
            
            cursor.execute(query, params)
            total = cursor.fetchone()['count']
            
            # স্টুডেন্ট তথ্য
            query = "SELECT id, telegram_id, username, student_email, full_name, university_name, account_status, credit_balance, created_at FROM student WHERE 1=1"
            params = []
            
            if search:
                query += " AND (student_email LIKE ? OR full_name LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])
            
            if status_filter:
                query += " AND account_status = ?"
                params.append(status_filter)
            
            query += " LIMIT ? OFFSET ?"
            offset = (page - 1) * per_page
            params.extend([per_page, offset])
            
            cursor.execute(query, params)
            students = cursor.fetchall()
            
            # ডাটা ফরম্যাট করুন
            students_data = [
                {
                    'id': s['id'],
                    'telegram_id': s['telegram_id'],
                    'username': s['username'],
                    'email': s['student_email'],
                    'name': s['full_name'],
                    'university': s['university_name'],
                    'status': s['account_status'],
                    'balance': f"${s['credit_balance']:.2f}",
                    'created_at': s['created_at']
                }
                for s in students
            ]
            
            return jsonify({
                'success': True,
                'data': students_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            })
    except Exception as e:
        logger.error(f"স্টুডেন্ট ডাটা ত্রুটি: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/student/<int:student_id>')
@login_required
def get_student(student_id):
    """
    নির্দিষ্ট স্টুডেন্টের বিস্তারিত তথ্য
    """
    try:
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
            student = cursor.fetchone()
            
            if not student:
                return jsonify({'success': False, 'error': 'স্টুডেন্ট খুঁজে পাওয়া যায়নি'}), 404
            
            # ক্রেডিট ইতিহাস
            cursor.execute(
                "SELECT * FROM credit_transaction WHERE student_id = ? ORDER BY created_at DESC LIMIT 10",
                (student_id,)
            )
            transactions = cursor.fetchall()
            
            student_data = dict(student)
            student_data['transactions'] = [
                {
                    'type': t['transaction_type'],
                    'amount': f"${t['amount']:.2f}",
                    'balance': f"${t['balance_after']:.2f}",
                    'date': t['created_at']
                }
                for t in transactions
            ]
            
            return jsonify({'success': True, 'data': student_data})
    except Exception as e:
        logger.error(f"স্টুডেন্ট ডিটেইলস ত্রুটি: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/student/<int:student_id>/credit', methods=['POST'])
@login_required
def adjust_credit(student_id):
    """
    স্টুডেন্ট ক্রেডিট সমন্বয় করুন
    """
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        action = data.get('action', 'add')  # add or subtract
        description = data.get('description', 'এডমিন সমন্বয়')
        
        if amount <= 0:
            return jsonify({'success': False, 'error': 'অবৈধ পরিমাণ'}), 400
        
        # ডাটাবেসে স্টুডেন্ট চেক করুন
        student = db.get_student(student_email=None, username=None, telegram_id=None)
        if not student:
            return jsonify({'success': False, 'error': 'স্টুডেন্ট খুঁজে পাওয়া যায়নি'}), 404
        
        if action == 'add':
            success = db.add_credit(
                student_id, amount, 'admin_adjustment',
                description, session.get('admin_id')
            )
        else:
            success = db.deduct_credit(
                student_id, amount, 'admin_adjustment',
                description
            )
        
        if success:
            logger.info(f"এডমিন ক্রেডিট সমন্বয়: ছাত্র {student_id}, পরিমাণ ${amount}")
            return jsonify({'success': True, 'message': 'ক্রেডিট সফলভাবে সমন্বয় করা হয়েছে'})
        else:
            return jsonify({'success': False, 'error': 'ক্রেডিট সমন্বয় ব্যর্থ'}), 500
    except Exception as e:
        logger.error(f"ক্রেডিট সমন্বয় ত্রুটি: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/student/<int:student_id>/suspend', methods=['POST'])
@login_required
def suspend_student(student_id):
    """
    স্টুডেন্ট অ্যাকাউন্ট সাসপেন্ড করুন
    """
    try:
        with db.get_cursor() as cursor:
            cursor.execute(
                "UPDATE student SET account_status = 'suspended' WHERE id = ?",
                (student_id,)
            )
            
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'error': 'স্টুডেন্ট খুঁজে পাওয়া যায়নি'}), 404
            
            logger.info(f"এডমিন স্টুডেন্ট সাসপেন্ড করেছেন: {student_id}")
            return jsonify({'success': True, 'message': 'স্টুডেন্ট সাসপেন্ড করা হয়েছে'})
    except Exception as e:
        logger.error(f"সাসপেন্ড ত্রুটি: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports')
@login_required
def get_reports():
    """
    সিস্টেম রিপোর্ট API
    """
    try:
        report_type = request.args.get('type', 'summary')
        
        with db.get_cursor() as cursor:
            if report_type == 'credit':
                # ক্রেডিট রিপোর্ট
                cursor.execute(
                    """SELECT 
                        DATE(created_at) as date,
                        transaction_type,
                        COUNT(*) as count,
                        SUM(amount) as total
                    FROM credit_transaction
                    GROUP BY DATE(created_at), transaction_type
                    ORDER BY date DESC
                    LIMIT 30"""
                )
                data = cursor.fetchall()
            elif report_type == 'students':
                # স্টুডেন্ট রিপোর্ট
                cursor.execute(
                    """SELECT 
                        account_status,
                        COUNT(*) as count,
                        AVG(credit_balance) as avg_balance
                    FROM student
                    GROUP BY account_status"""
                )
                data = cursor.fetchall()
            else:
                # সামারি রিপোর্ট
                cursor.execute("SELECT COUNT(*) as students FROM student")
                students = cursor.fetchone()
                cursor.execute("SELECT SUM(credit_balance) as total FROM student")
                balance = cursor.fetchone()
                cursor.execute("SELECT COUNT(*) as works FROM work_board")
                works = cursor.fetchone()
                
                data = {
                    'total_students': students['students'],
                    'total_balance': balance['total'] or 0,
                    'total_works': works['works']
                }
            
            return jsonify({'success': True, 'data': data})
    except Exception as e:
        logger.error(f"রিপোর্ট ত্রুটি: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """404 ত্রুটি হ্যান্ডেলার"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 ত্রুটি হ্যান্ডেলার"""
    logger.error(f"সার্ভার ত্রুটি: {e}")
    return render_template('500.html'), 500


def run_server(host=SERVER_HOST, port=SERVER_PORT, debug=FLASK_ENV == 'development'):
    """
    Flask সার্ভার চালান
    """
    db.connect()
    print(f"""
╔══════════════════════════════════════════════════════╗
║ 🎓 SI STUDENT ACCOUNT - এডমিন প্যানেল            ║
║ 🌐 সার্ভার চলছে: http://{host}:{port}                ║
║ 📊 ড্যাশবোর্ড: http://{host}:{port}/dashboard         ║
╚══════════════════════════════════════════════════════╝
    """)
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
