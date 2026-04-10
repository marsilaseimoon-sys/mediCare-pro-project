from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'medicare_pro_secret_2026'
DB = os.path.join(os.path.dirname(__file__), 'medicare_pro.db')


# ─── DB SETUP ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age TEXT,
        gender TEXT,
        phone TEXT,
        disease TEXT,
        blood_group TEXT,
        address TEXT,
        status TEXT DEFAULT 'Active',
        reg_date TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER DEFAULT 0,
        price REAL DEFAULT 0,
        sold INTEGER DEFAULT 0,
        category TEXT,
        expiry TEXT,
        supplier TEXT,
        reorder_level INTEGER DEFAULT 50,
        added_date TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient TEXT,
        amount REAL,
        method TEXT,
        payment_type TEXT,
        status TEXT DEFAULT 'Paid',
        pay_date TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        date TEXT,
        time TEXT,
        doctor TEXT,
        reason TEXT,
        visit_type TEXT DEFAULT 'In-Clinic',
        status TEXT DEFAULT 'Pending',
        booked_on TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        phone TEXT,
        email TEXT,
        qualification TEXT,
        experience TEXT,
        schedule TEXT,
        fee REAL DEFAULT 0,
        status TEXT DEFAULT 'Active',
        joined_date TEXT DEFAULT (datetime('now','localtime'))
    );
    """)
    db.commit()
    # Seed sample data if empty
    cur = db.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        _seed_data(db)
    db.close()


def _seed_data(db):
    db.executemany(
        "INSERT INTO patients(name,age,gender,phone,disease,blood_group,address,status) VALUES(?,?,?,?,?,?,?,?)",
        [
            ("Michael Rodriguez", "42", "Male", "+1 (212) 555-0182", "Hypertension", "O+", "New York, NY", "Active"),
            ("Linda Park", "35", "Female", "+1 (310) 555-0247", "Eczema", "A+", "Los Angeles, CA", "Follow-Up"),
            ("David Walsh", "58", "Male", "+1 (415) 555-0391", "Atrial Fibrillation", "B-", "San Francisco, CA", "Active"),
            ("Sophia Anderson", "28", "Female", "+1 (646) 555-0415", "General Checkup", "AB+", "Brooklyn, NY", "Discharged"),
            ("Kevin Patel", "47", "Male", "+1 (718) 555-0528", "Disc Herniation", "O-", "Queens, NY", "Follow-Up"),
            ("Grace Thompson", "31", "Female", "+1 (213) 555-0674", "Migraine", "A-", "Los Angeles, CA", "Active"),
            ("James Nguyen", "52", "Male", "+1 (312) 555-0711", "Type 2 Diabetes", "B+", "Chicago, IL", "Active"),
            ("Emma Wilson", "6", "Female", "+1 (404) 555-0823", "Asthma", "O+", "Atlanta, GA", "Active"),
        ]
    )
    db.executemany(
        "INSERT INTO doctors(name,specialization,phone,qualification,experience,schedule,fee,status) VALUES(?,?,?,?,?,?,?,?)",
        [
            ("James Harrington", "Cardiologist", "+1 (212) 555-1001", "MBBS, MD (Cardiology), FACC", "14", "Mon-Fri 9AM-6PM", 250.0, "Active"),
            ("Sarah Mitchell", "Dermatologist", "+1 (212) 555-1002", "MBBS, MRCP (Dermatology)", "10", "Mon-Sat 9AM-5PM", 180.0, "Active"),
            ("Robert Chen", "Orthopedic Surgeon", "+1 (212) 555-1003", "MBBS, MS (Orthopedics), FACS", "18", "Mon-Wed-Fri", 300.0, "Active"),
            ("Amelia Foster", "Pediatrician", "+1 (212) 555-1004", "MBBS, DCH, MRCPCH", "9", "Mon-Fri 9AM-5PM", 150.0, "Active"),
            ("Marcus Williams", "Neurologist", "+1 (212) 555-1005", "MBBS, MD (Neurology), DM", "16", "Tue-Thu-Sat", 280.0, "Active"),
            ("Priya Sharma", "General Physician", "+1 (212) 555-1006", "MBBS, MRCP (Internal Med)", "7", "Mon-Sat 9AM-6PM", 120.0, "Active"),
        ]
    )
    db.executemany(
        "INSERT INTO medicines(name,category,quantity,price,expiry,supplier,reorder_level) VALUES(?,?,?,?,?,?,?)",
        [
            ("Amoxicillin 500mg", "Antibiotic", 12, 8.50, "2025-06-30", "Pfizer Inc.", 50),
            ("Warfarin 5mg", "Anticoagulant", 8, 15.00, "2025-09-15", "Bristol-Myers Squibb", 30),
            ("Metformin 1000mg", "Antidiabetic", 280, 5.25, "2026-12-01", "Teva Pharmaceuticals", 100),
            ("Metoprolol 50mg", "Beta Blocker", 31, 9.75, "2026-08-20", "AstraZeneca", 60),
            ("Paracetamol 500mg", "Analgesic", 840, 2.50, "2027-03-15", "GlaxoSmithKline", 200),
            ("Ceftriaxone 1g", "Antibiotic", 6, 32.00, "2025-04-10", "Roche Pharma", 20),
            ("Insulin Glargine", "Antidiabetic", 24, 55.00, "2025-11-25", "Sanofi", 40),
            ("Atorvastatin 40mg", "Antihypertensive", 195, 12.00, "2026-07-14", "Pfizer Inc.", 80),
            ("Salbutamol Inhaler", "Bronchodilator", 45, 18.50, "2025-12-31", "GlaxoSmithKline", 30),
            ("Ibuprofen 400mg", "Analgesic", 380, 3.20, "2027-08-10", "Abbott Labs", 100),
        ]
    )
    db.executemany(
        "INSERT INTO payments(patient,amount,payment_type,method,status) VALUES(?,?,?,?,?)",
        [
            ("Michael Rodriguez", 250.0, "Consultation", "Card", "Paid"),
            ("Linda Park", 130.0, "Consultation", "Online", "Paid"),
            ("David Walsh", 280.0, "Consultation", "Cash", "Pending"),
            ("Sophia Anderson", 150.0, "Consultation", "Insurance", "Paid"),
            ("Kevin Patel", 135.0, "Consultation", "Card", "Failed"),
            ("Grace Thompson", 250.0, "Consultation", "Cash", "Paid"),
            ("James Nguyen", 45.0, "Pharmacy", "Cash", "Paid"),
            ("Emma Wilson", 320.0, "Lab Test", "Insurance", "Paid"),
        ]
    )
    db.executemany(
        "INSERT INTO bookings(name,phone,doctor,date,time,reason,visit_type,status) VALUES(?,?,?,?,?,?,?,?)",
        [
            ("Michael Rodriguez", "+1 (212) 555-0182", "Dr. James Harrington", "2026-03-15", "09:00 AM", "Cardiac follow-up", "In-Clinic", "Confirmed"),
            ("Linda Park", "+1 (310) 555-0247", "Dr. Sarah Mitchell", "2026-03-15", "09:30 AM", "Eczema review", "Video", "Confirmed"),
            ("David Walsh", "+1 (415) 555-0391", "Dr. Marcus Williams", "2026-03-15", "10:00 AM", "Migraine assessment", "In-Clinic", "Pending"),
            ("Sophia Anderson", "+1 (646) 555-0415", "Dr. Amelia Foster", "2026-03-15", "10:30 AM", "Wellness checkup", "In-Clinic", "Confirmed"),
            ("Kevin Patel", "+1 (718) 555-0528", "Dr. Robert Chen", "2026-03-16", "11:00 AM", "Post-surgery consult", "Phone", "Pending"),
            ("Grace Thompson", "+1 (213) 555-0674", "Dr. James Harrington", "2026-03-16", "11:30 AM", "BP monitoring", "In-Clinic", "Confirmed"),
        ]
    )
    db.commit()


# ─── CONTEXT PROCESSOR ───────────────────────────────────────────────────────

from urllib.parse import quote as url_quote

@app.template_filter('urlencode')
def urlencode_filter(s):
    return url_quote(str(s))

@app.context_processor
def inject_stats():
    from datetime import datetime
    now = datetime.now().strftime("%A, %d %B %Y · %I:%M %p")
    db = get_db()
    stats = {
        'total_patients': db.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
        'active_doctors': db.execute("SELECT COUNT(*) FROM doctors WHERE status='Active'").fetchone()[0],
        'pending_bookings': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Pending'").fetchone()[0],
        'low_stock': db.execute("SELECT COUNT(*) FROM medicines WHERE quantity <= 10").fetchone()[0],
        'total_revenue': db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Paid'").fetchone()[0],
    }
    db.close()
    return dict(nav_stats=stats, now=now)


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    db = get_db()
    recent = db.execute(
        "SELECT * FROM patients ORDER BY id DESC LIMIT 8"
    ).fetchall()
    today_appts = db.execute(
        "SELECT * FROM bookings ORDER BY date DESC LIMIT 6"
    ).fetchall()
    db.close()
    return render_template('dashboard.html', recent=recent, today_appts=today_appts)


# ── PATIENTS ──────────────────────────────────────────────────────────────────

@app.route('/patients')
def patients():
    db = get_db()
    q = request.args.get('q', '')
    gender = request.args.get('gender', '')
    status = request.args.get('status', '')
    sql = "SELECT * FROM patients WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR phone LIKE ? OR disease LIKE ?)"
        params += [f'%{q}%', f'%{q}%', f'%{q}%']
    if gender:
        sql += " AND gender=?"
        params.append(gender)
    if status:
        sql += " AND status=?"
        params.append(status)
    sql += " ORDER BY id DESC"
    rows = db.execute(sql, params).fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
        'active': db.execute("SELECT COUNT(*) FROM patients WHERE status='Active'").fetchone()[0],
        'followup': db.execute("SELECT COUNT(*) FROM patients WHERE status='Follow-Up'").fetchone()[0],
        'discharged': db.execute("SELECT COUNT(*) FROM patients WHERE status='Discharged'").fetchone()[0],
    }
    db.close()
    return render_template('patients.html', patients=rows, stats=stats, q=q, gender=gender, status=status)


@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO patients(name,age,gender,blood_group,phone,disease,address,status) VALUES(?,?,?,?,?,?,?,?)",
            (request.form['name'], request.form['age'], request.form['gender'],
             request.form['blood_group'], request.form['phone'],
             request.form['disease'], request.form['address'],
             request.form.get('status', 'Active'))
        )
        db.commit()
        db.close()
        flash('Patient registered successfully!', 'success')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', patient=None, action='Add')


@app.route('/patients/edit/<int:pid>', methods=['GET', 'POST'])
def edit_patient(pid):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE patients SET name=?,age=?,gender=?,blood_group=?,phone=?,disease=?,address=?,status=? WHERE id=?",
            (request.form['name'], request.form['age'], request.form['gender'],
             request.form['blood_group'], request.form['phone'],
             request.form['disease'], request.form['address'],
             request.form.get('status', 'Active'), pid)
        )
        db.commit()
        db.close()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients'))
    patient = db.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    db.close()
    return render_template('patient_form.html', patient=patient, action='Edit')


@app.route('/patients/delete/<int:pid>', methods=['POST'])
def delete_patient(pid):
    db = get_db()
    db.execute("DELETE FROM patients WHERE id=?", (pid,))
    db.commit()
    db.close()
    flash('Patient deleted.', 'info')
    return redirect(url_for('patients'))


# ── DOCTORS ───────────────────────────────────────────────────────────────────

@app.route('/doctors')
def doctors():
    db = get_db()
    rows = db.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
        'active': db.execute("SELECT COUNT(*) FROM doctors WHERE status='Active'").fetchone()[0],
        'on_leave': db.execute("SELECT COUNT(*) FROM doctors WHERE status='On Leave'").fetchone()[0],
    }
    db.close()
    return render_template('doctors.html', doctors=rows, stats=stats)


@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO doctors(name,specialization,qualification,experience,phone,email,schedule,fee,status) VALUES(?,?,?,?,?,?,?,?,?)",
            (request.form['name'], request.form['specialization'],
             request.form['qualification'], request.form['experience'],
             request.form['phone'], request.form['email'],
             request.form['schedule'], float(request.form.get('fee', 0)),
             request.form.get('status', 'Active'))
        )
        db.commit()
        db.close()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors'))
    return render_template('doctor_form.html', doctor=None, action='Add')


@app.route('/doctors/edit/<int:did>', methods=['GET', 'POST'])
def edit_doctor(did):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE doctors SET name=?,specialization=?,qualification=?,experience=?,phone=?,email=?,schedule=?,fee=?,status=? WHERE id=?",
            (request.form['name'], request.form['specialization'],
             request.form['qualification'], request.form['experience'],
             request.form['phone'], request.form['email'],
             request.form['schedule'], float(request.form.get('fee', 0)),
             request.form.get('status', 'Active'), did)
        )
        db.commit()
        db.close()
        flash('Doctor updated!', 'success')
        return redirect(url_for('doctors'))
    doctor = db.execute("SELECT * FROM doctors WHERE id=?", (did,)).fetchone()
    db.close()
    return render_template('doctor_form.html', doctor=doctor, action='Edit')


@app.route('/doctors/delete/<int:did>', methods=['POST'])
def delete_doctor(did):
    db = get_db()
    db.execute("DELETE FROM doctors WHERE id=?", (did,))
    db.commit()
    db.close()
    flash('Doctor removed.', 'info')
    return redirect(url_for('doctors'))


# ── MEDICINES ─────────────────────────────────────────────────────────────────

@app.route('/medicines')
def medicines():
    db = get_db()
    q = request.args.get('q', '')
    cat = request.args.get('category', '')
    stock = request.args.get('stock', '')
    sql = "SELECT * FROM medicines WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR category LIKE ? OR supplier LIKE ?)"
        params += [f'%{q}%', f'%{q}%', f'%{q}%']
    if cat:
        sql += " AND category=?"
        params.append(cat)
    if stock == 'critical':
        sql += " AND quantity <= 10"
    elif stock == 'low':
        sql += " AND quantity > 10 AND quantity <= 50"
    elif stock == 'ok':
        sql += " AND quantity > 50"
    sql += " ORDER BY id DESC"
    rows = db.execute(sql, params).fetchall()
    cats = db.execute("SELECT DISTINCT category FROM medicines ORDER BY category").fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM medicines").fetchone()[0],
        'total_stock': db.execute("SELECT COALESCE(SUM(quantity),0) FROM medicines").fetchone()[0],
        'critical': db.execute("SELECT COUNT(*) FROM medicines WHERE quantity <= 10").fetchone()[0],
        'low': db.execute("SELECT COUNT(*) FROM medicines WHERE quantity > 10 AND quantity <= 50").fetchone()[0],
        'revenue': db.execute("SELECT COALESCE(SUM(sold*price),0) FROM medicines").fetchone()[0],
    }
    db.close()
    return render_template('medicines.html', medicines=rows, stats=stats,
                           categories=cats, q=q, category=cat, stock=stock)


@app.route('/medicines/add', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO medicines(name,category,quantity,price,expiry,supplier,reorder_level) VALUES(?,?,?,?,?,?,?)",
            (request.form['name'], request.form['category'],
             int(request.form.get('quantity', 0)),
             float(request.form.get('price', 0)),
             request.form['expiry'], request.form['supplier'],
             int(request.form.get('reorder_level', 50)))
        )
        db.commit()
        db.close()
        flash('Medicine added to inventory!', 'success')
        return redirect(url_for('medicines'))
    return render_template('medicine_form.html', medicine=None, action='Add')


@app.route('/medicines/edit/<int:mid>', methods=['GET', 'POST'])
def edit_medicine(mid):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE medicines SET name=?,category=?,quantity=?,price=?,expiry=?,supplier=?,reorder_level=? WHERE id=?",
            (request.form['name'], request.form['category'],
             int(request.form.get('quantity', 0)),
             float(request.form.get('price', 0)),
             request.form['expiry'], request.form['supplier'],
             int(request.form.get('reorder_level', 50)), mid)
        )
        db.commit()
        db.close()
        flash('Medicine updated!', 'success')
        return redirect(url_for('medicines'))
    med = db.execute("SELECT * FROM medicines WHERE id=?", (mid,)).fetchone()
    db.close()
    return render_template('medicine_form.html', medicine=med, action='Edit')


@app.route('/medicines/sell/<int:mid>', methods=['POST'])
def sell_medicine(mid):
    qty = int(request.form.get('quantity', 1))
    db = get_db()
    med = db.execute("SELECT * FROM medicines WHERE id=?", (mid,)).fetchone()
    if med and med['quantity'] >= qty:
        db.execute("UPDATE medicines SET quantity=quantity-?, sold=sold+? WHERE id=?", (qty, qty, mid))
        db.commit()
        flash(f'Sold {qty} units of {med["name"]}!', 'success')
    else:
        flash('Insufficient stock!', 'error')
    db.close()
    return redirect(url_for('medicines'))


@app.route('/medicines/delete/<int:mid>', methods=['POST'])
def delete_medicine(mid):
    db = get_db()
    db.execute("DELETE FROM medicines WHERE id=?", (mid,))
    db.commit()
    db.close()
    flash('Medicine removed.', 'info')
    return redirect(url_for('medicines'))


# ── PAYMENTS ──────────────────────────────────────────────────────────────────

@app.route('/payments')
def payments():
    db = get_db()
    q = request.args.get('q', '')
    status = request.args.get('status', '')
    method = request.args.get('method', '')
    sql = "SELECT * FROM payments WHERE 1=1"
    params = []
    if q:
        sql += " AND (patient LIKE ? OR payment_type LIKE ?)"
        params += [f'%{q}%', f'%{q}%']
    if status:
        sql += " AND status=?"
        params.append(status)
    if method:
        sql += " AND method=?"
        params.append(method)
    sql += " ORDER BY id DESC"
    rows = db.execute(sql, params).fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM payments").fetchone()[0],
        'paid': db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Paid'").fetchone()[0],
        'pending': db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Pending'").fetchone()[0],
        'refunded': db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Refunded'").fetchone()[0],
    }
    db.close()
    return render_template('payments.html', payments=rows, stats=stats, q=q, status=status, method=method)


@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "INSERT INTO payments(patient,amount,payment_type,method,status) VALUES(?,?,?,?,?)",
            (request.form['patient'], float(request.form.get('amount', 0)),
             request.form['payment_type'], request.form['method'],
             request.form.get('status', 'Paid'))
        )
        db.commit()
        db.close()
        flash('Payment recorded!', 'success')
        return redirect(url_for('payments'))
    patients = db.execute("SELECT name FROM patients ORDER BY name").fetchall()
    db.close()
    return render_template('payment_form.html', patients=patients)


@app.route('/payments/delete/<int:pid>', methods=['POST'])
def delete_payment(pid):
    db = get_db()
    db.execute("DELETE FROM payments WHERE id=?", (pid,))
    db.commit()
    db.close()
    flash('Payment record deleted.', 'info')
    return redirect(url_for('payments'))


# ── APPOINTMENTS ──────────────────────────────────────────────────────────────

@app.route('/appointments')
def appointments():
    db = get_db()
    q = request.args.get('q', '')
    status = request.args.get('status', '')
    date_filter = request.args.get('date', '')
    sql = "SELECT * FROM bookings WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR doctor LIKE ? OR reason LIKE ?)"
        params += [f'%{q}%', f'%{q}%', f'%{q}%']
    if status:
        sql += " AND status=?"
        params.append(status)
    if date_filter:
        sql += " AND date=?"
        params.append(date_filter)
    sql += " ORDER BY date DESC, time"
    rows = db.execute(sql, params).fetchall()
    stats = {
        'total': db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0],
        'confirmed': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Confirmed'").fetchone()[0],
        'pending': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Pending'").fetchone()[0],
        'cancelled': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Cancelled'").fetchone()[0],
        'completed': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Completed'").fetchone()[0],
    }
    db.close()
    return render_template('appointments.html', appointments=rows, stats=stats,
                           q=q, status=status, date_filter=date_filter)


@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "INSERT INTO bookings(name,phone,doctor,date,time,reason,visit_type,status) VALUES(?,?,?,?,?,?,?,?)",
            (request.form['name'], request.form['phone'], request.form['doctor'],
             request.form['date'], request.form['time'],
             request.form['reason'], request.form.get('visit_type', 'In-Clinic'),
             request.form.get('status', 'Pending'))
        )
        db.commit()
        db.close()
        flash('Appointment booked!', 'success')
        return redirect(url_for('appointments'))
    patients = db.execute("SELECT name FROM patients ORDER BY name").fetchall()
    doctors = db.execute("SELECT name, specialization FROM doctors WHERE status='Active' ORDER BY name").fetchall()
    db.close()
    return render_template('appointment_form.html', patients=patients, doctors=doctors, appointment=None, action='Book')


@app.route('/appointments/status/<int:aid>', methods=['POST'])
def update_appointment_status(aid):
    new_status = request.form.get('status')
    db = get_db()
    db.execute("UPDATE bookings SET status=? WHERE id=?", (new_status, aid))
    db.commit()
    db.close()
    flash(f'Appointment status updated to {new_status}!', 'success')
    return redirect(url_for('appointments'))


@app.route('/appointments/delete/<int:aid>', methods=['POST'])
def delete_appointment(aid):
    db = get_db()
    db.execute("DELETE FROM bookings WHERE id=?", (aid,))
    db.commit()
    db.close()
    flash('Appointment deleted.', 'info')
    return redirect(url_for('appointments'))


# ── PUBLIC PAGES ──────────────────────────────────────────────────────────────

@app.route('/home')
def home():
    db = get_db()
    doctors_list = db.execute("SELECT * FROM doctors WHERE status='Active' ORDER BY id LIMIT 4").fetchall()
    db.close()
    return render_template('home.html', doctors=doctors_list)


@app.route('/find-doctors')
def find_doctors():
    db = get_db()
    q = request.args.get('q', '')
    spec = request.args.get('spec', '')
    sql = "SELECT * FROM doctors WHERE status='Active'"
    params = []
    if q:
        sql += " AND (name LIKE ? OR specialization LIKE ?)"
        params += [f'%{q}%', f'%{q}%']
    if spec:
        sql += " AND specialization=?"
        params.append(spec)
    sql += " ORDER BY name"
    rows = db.execute(sql, params).fetchall()
    specs = db.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization").fetchall()
    db.close()
    return render_template('find_doctors.html', doctors=rows, specializations=specs, q=q, spec=spec)


@app.route('/doctor/<int:did>')
def doctor_profile(did):
    db = get_db()
    doctor = db.execute("SELECT * FROM doctors WHERE id=?", (did,)).fetchone()
    db.close()
    if not doctor:
        return redirect(url_for('find_doctors'))
    return render_template('doctor_profile.html', doctor=doctor)


@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "INSERT INTO bookings(name,phone,doctor,date,time,reason,visit_type,status) VALUES(?,?,?,?,?,?,?,?)",
            (request.form['name'], request.form['phone'], request.form['doctor'],
             request.form['date'], request.form['time'],
             request.form['reason'], request.form.get('visit_type', 'In-Clinic'), 'Pending')
        )
        db.commit()
        db.close()
        flash('Appointment booked successfully! We will confirm shortly.', 'success')
        return redirect(url_for('book_appointment'))
    doctors = db.execute("SELECT * FROM doctors WHERE status='Active' ORDER BY name").fetchall()
    db.close()
    return render_template('book_appointment.html', doctors=doctors)


# ── API ENDPOINTS ─────────────────────────────────────────────────────────────

@app.route('/api/stats')
def api_stats():
    db = get_db()
    data = {
        'patients': db.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
        'doctors': db.execute("SELECT COUNT(*) FROM doctors WHERE status='Active'").fetchone()[0],
        'appointments': db.execute("SELECT COUNT(*) FROM bookings WHERE status='Pending'").fetchone()[0],
        'revenue': db.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='Paid'").fetchone()[0],
        'low_stock': db.execute("SELECT COUNT(*) FROM medicines WHERE quantity <= 10").fetchone()[0],
    }
    db.close()
    return jsonify(data)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
