# MediCare Pro — Flask Healthcare Management System

> A full-stack web application for managing hospital/clinic operations — built with Python Flask + SQLite.

---

## Project Structure

```
medicare_pro/
├── app.py                    ← Main Flask app (all routes + DB logic)
├── medicare_pro.db           ← SQLite database (auto-created on first run)
├── static/                   ← Static assets folder (add CSS/JS/images here if needed)
└── templates/
    ├── base.html             ← Master layout (sidebar, topbar, shared CSS)
    │
    ├── ── Admin Panel ──
    ├── dashboard.html        ← Admin dashboard with live stats
    ├── patients.html         ← Patient records list (search + filter)
    ├── patient_form.html     ← Add / Edit patient form
    ├── doctors.html          ← Doctor directory (card view)
    ├── doctor_form.html      ← Add / Edit doctor form
    ├── medicines.html        ← Pharmacy inventory (search + filter + sell)
    ├── medicine_form.html    ← Add / Edit medicine form
    ├── payments.html         ← Payment history (filter by status/method)
    ├── payment_form.html     ← Record new payment form
    ├── appointments.html     ← Appointment schedule (filter + status update)
    ├── appointment_form.html ← Book / Edit appointment form
    │
    └── ── Public Pages ──
        ├── home.html             ← Public landing page
        ├── find_doctors.html     ← Browse & filter doctors (public)
        ├── doctor_profile.html   ← Individual doctor profile (public)
        └── book_appointment.html ← Public appointment booking form
```

---

## Requirements

- **Python 3.8+**
- **Flask** (only external dependency)

---

## Installation & Run

### Step 1 — Install Flask

```bash
pip install flask
```

### Step 2 — Run the app

```bash
cd medicare_pro
python app.py
```

### Step 3 — Open in browser

```
http://localhost:5000
```

The SQLite database (`medicare_pro.db`) is created automatically with sample data on first run.

---

## Pages & Routes

### Admin Panel

| Route | Page | Description |
|---|---|---|
| `/` | Redirect | Redirects to `/dashboard` |
| `/dashboard` | Dashboard | Live stats: patients, doctors, revenue, alerts |
| `/patients` | Patient Records | List, search, filter by gender/status |
| `/patients/add` | Add Patient | Register new patient |
| `/patients/edit/<id>` | Edit Patient | Update patient details |
| `/patients/delete/<id>` | Delete Patient | Remove patient record |
| `/doctors` | Doctor Directory | Card view of all doctors |
| `/doctors/add` | Add Doctor | Register new doctor |
| `/doctors/edit/<id>` | Edit Doctor | Update doctor profile |
| `/doctors/delete/<id>` | Delete Doctor | Remove doctor |
| `/medicines` | Pharmacy Inventory | List with stock alerts + sell button |
| `/medicines/add` | Add Medicine | Add new medicine to inventory |
| `/medicines/edit/<id>` | Edit Medicine | Update medicine details |
| `/medicines/sell/<id>` | Sell Medicine | Deduct stock quantity (POST) |
| `/medicines/delete/<id>` | Delete Medicine | Remove from inventory |
| `/payments` | Payment History | All transactions, filter by status/method |
| `/payments/add` | Record Payment | Log a new payment |
| `/payments/delete/<id>` | Delete Payment | Remove payment record |
| `/appointments` | Appointments | Schedule view, confirm/cancel/delete |
| `/appointments/add` | Book Appointment | Admin appointment booking |
| `/appointments/status/<id>` | Update Status | Quick confirm or cancel (POST) |
| `/appointments/delete/<id>` | Delete Appointment | Remove appointment |

### Public Pages

| Route | Page | Description |
|---|---|---|
| `/home` | Landing Page | Public homepage with featured doctors |
| `/find-doctors` | Find Doctors | Browse & search all active doctors |
| `/doctor/<id>` | Doctor Profile | Individual doctor detail page |
| `/book` | Book Appointment | Public booking form (no login needed) |

### API

| Route | Returns |
|---|---|
| `/api/stats` | JSON — patients, doctors, pending appointments, revenue, low stock count |

---

## Database Tables

Database is SQLite and auto-created at `medicare_pro/medicare_pro.db`.

### patients
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Full name |
| age | TEXT | Age |
| gender | TEXT | Male / Female / Other |
| phone | TEXT | Contact number |
| disease | TEXT | Diagnosis / symptom |
| blood_group | TEXT | e.g. O+, A- |
| address | TEXT | City/address |
| status | TEXT | Active / Follow-Up / Discharged |
| reg_date | TEXT | Registration timestamp |

### doctors
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Full name (without Dr.) |
| specialization | TEXT | e.g. Cardiologist |
| phone | TEXT | Contact |
| email | TEXT | Email address |
| qualification | TEXT | e.g. MBBS, MD |
| experience | TEXT | Years of experience |
| schedule | TEXT | e.g. Mon-Fri 9AM-5PM |
| fee | REAL | Consultation fee in $ |
| status | TEXT | Active / On Leave / Resigned |
| joined_date | TEXT | Date added |

### medicines
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Medicine name + strength |
| quantity | INTEGER | Current stock units |
| price | REAL | Unit price in $ |
| sold | INTEGER | Total units sold |
| category | TEXT | e.g. Antibiotic, Analgesic |
| expiry | TEXT | Expiry date (YYYY-MM-DD) |
| supplier | TEXT | Supplier name |
| reorder_level | INTEGER | Alert threshold (default 50) |
| added_date | TEXT | Date added |

### payments
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| patient | TEXT | Patient name |
| amount | REAL | Amount in $ |
| method | TEXT | Cash / Card / Insurance / Online / Easypaisa / JazzCash |
| payment_type | TEXT | Consultation / Pharmacy / Lab Test / Surgery / Emergency |
| status | TEXT | Paid / Pending / Failed / Refunded / Partial |
| pay_date | TEXT | Payment timestamp |

### bookings (Appointments)
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Patient name |
| phone | TEXT | Contact number |
| date | TEXT | Appointment date (YYYY-MM-DD) |
| time | TEXT | e.g. 09:00 AM |
| doctor | TEXT | Doctor name (with Dr. prefix) |
| reason | TEXT | Reason for visit / notes |
| visit_type | TEXT | In-Clinic / Video / Phone |
| status | TEXT | Pending / Confirmed / Cancelled / Completed / Rescheduled |
| booked_on | TEXT | Booking timestamp |

---

## Sample Data (Auto-seeded on first run)

- 8 patients — Michael Rodriguez, Linda Park, David Walsh, and more
- 6 doctors — Cardiologist, Dermatologist, Orthopedic Surgeon, Pediatrician, Neurologist, General Physician
- 10 medicines — Amoxicillin, Metformin, Paracetamol, Insulin, Atorvastatin, and more
- 8 payment records
- 6 appointments

To reset all data, delete `medicare_pro.db` and restart — it will regenerate automatically.

---

## Features

- Dashboard with real-time stats (patients, doctors, revenue, low stock, pending bookings)
- Patient Management — full CRUD, search by name/phone/disease, filter by gender and status
- Doctor Management — card-based directory, full CRUD, public doctor profile pages
- Pharmacy Inventory — add/edit/delete medicines, sell with auto stock deduction, critical stock alerts
- Payment Tracking — record payments, filter by status and payment method
- Appointment System — book, confirm, cancel, delete; filter by date/status; public booking form
- Public Website — landing page, find doctors page, individual profiles, online booking
- REST API endpoint at `/api/stats` returning live JSON stats
- Flash messages for all success/error/info actions
- Professional dark theme UI with teal accent, fully responsive

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite (built-in sqlite3 library) |
| Frontend | HTML5, CSS3 (embedded in base.html), Jinja2 templates |
| Fonts | Sora + Instrument Serif via Google Fonts |

---

## Deployment

### Render or Railway
Create `requirements.txt`:
```
flask
gunicorn
```
Start command: `gunicorn app:app`

### PythonAnywhere
Upload the `medicare_pro/` folder, set WSGI to point to `app.py`, and run.

---

## Notes

- No login/authentication — can be added using Flask-Login
- No file uploads — can be extended for doctor photos, reports, etc.
- SQLite works well for development and demo; switch to PostgreSQL or MySQL for production
- The `static/` folder is empty — all styles are embedded in `base.html` for portability and easy deployment

---

## Author

**Marsellah Seimoon** — Full-Stack Developer & AI Engineer  
GitHub: github.com/marsellaseimoon  
Email: marsellaseimoon@gmail.com
