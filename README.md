# mediCare-pro-project
Full-stack Flask healthcare platform — patient records, doctor directory, appointments, pharmacy &amp; payments management.
# MediCare Pro — Flask Web Application

## Requirements
- Python 3.8+
- Flask (already installed)

## Install & Run
```bash
pip install flask
python app.py
```
Then open: http://localhost:5000

## Pages
### Admin Panel
- `/dashboard`     — Admin dashboard with stats
- `/patients`      — Patient records (add/edit/delete)
- `/doctors`       — Doctor directory (add/edit/delete)
- `/medicines`     — Pharmacy inventory (add/sell/delete)
- `/payments`      — Payment history (record/delete)
- `/appointments`  — Appointment schedule (book/confirm/cancel)

### Public Site
- `/home`          — Landing page
- `/find-doctors`  — Browse & filter doctors
- `/doctor/<id>`   — Individual doctor profile
- `/book`          — Public appointment booking form

## Database
SQLite — auto-created as `medicare_pro.db` on first run with sample data.
