# 🏗️ KaamSetu — Trusted Construction Work Platform

> **Built by a team of 20 senior full-stack developers**
> IIT Madras Hackathon 2025 — Web Development Domain

---

## 🎯 What is KaamSetu?

KaamSetu ("काम सेतु" — Bridge to Work) is a platform where construction workers build
verified profiles through completed, rated work — not self-reported claims.

- **Workers** don't write CVs. Their profile IS their job history.
- **Contractors** post jobs, hire from a trust-sorted list, endorse skills they actually observed.
- **Trust** is earned through small, verified interactions — not badges or self-description.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Seed demo data (for judging/demo)
```bash
python manage.py seed_demo
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser
- **Worker UI:** http://localhost:8000/worker/feed/
- **Contractor:** http://localhost:8000/contractor/dashboard/
- **Admin Panel:** http://localhost:8000/admin/

---

## 🔑 Demo Login Credentials

| Role | Phone | OTP (shown in console) |
|------|-------|------------------------|
| Worker (Mason) | 9876543201 | Shown in terminal |
| Worker (Electrician) | 9876543202 | Shown in terminal |
| Worker (Plumber) | 9876543203 | Shown in terminal |
| Contractor | 9876540001 | Shown in terminal |
| Admin | 0000000000 | Password: admin123 |

> **How OTP works in dev:** Enter any phone → OTP prints in the terminal → enter it in browser.
> No SMS cost during development.

---

## 🏗️ Architecture

```
kaamsetu/
├── config/              # Settings, URLs, WSGI
├── accounts/            # Phone-based OTP auth, custom User model
├── workers/             # Worker profiles, favourites
├── contractors/         # Contractor dashboard, post jobs, hire
├── jobs/                # Job model, feed, apply, complete
├── ratings/             # Immutable ratings + skill endorsements
├── notifications/       # SMS abstraction (console/Fast2SMS/Twilio)
├── core/                # Home redirect, seed command, trust logic
├── templates/
│   ├── auth/            # OTP login page
│   ├── worker/          # Icon-heavy, low-literacy UI
│   ├── contractor/      # Full dashboard UI
│   └── shared/          # Rate, endorse pages
└── static/
    ├── css/main.css     # Full design system
    └── js/main.js       # Voice UI, apply, hire, geolocation
```

---

## ⭐ Key Technical Decisions

### 1. Trust Score Algorithm
```python
trust_score = (avg_rating/5 * 50)       # 50 pts — quality
            + (unique_contractors * 2)   # 20 pts — diversity
            + (endorsement_count * 1)    # 20 pts — verified skills
            + (recency_boost)            # 10 pts — active recently
```

### 2. Immutable Ratings
Ratings use a custom `save()` override that raises `ValidationError` if `self.pk` exists.
No admin can edit them either — `has_change_permission` returns False.

### 3. Haversine Distance Matching
Pure Python Haversine formula for job-worker radius matching.
Ready to swap for PostGIS `dwithin` in production with zero view changes.

### 4. Two Distinct UIs
- **Worker UI:** Icon-only navigation, emoji-based job cards, voice readout via Web Speech API, one-tap apply, PWA manifest for Android install
- **Contractor UI:** Full text dashboard, smart applicant sorting, endorsement flow

### 5. Smart Applicant Sorting
```python
applications.annotate(
    avg_rating=Avg('worker__ratings_received__score'),
    completed_jobs=Count('worker__engagements', filter=Q(status='completed'))
).order_by('-is_past_collaborator', '-avg_rating', '-completed_jobs')
```

---

## 📱 PWA Support

Workers can install KaamSetu on their Android phone like an app:
- Open in Chrome → "Add to Home Screen"
- Works offline for profile viewing
- Push notifications ready (Celery + FCM in production)

---

## 📡 SMS Integration

Set in `.env`:
```
SMS_PROVIDER=console       # dev — prints to terminal
SMS_PROVIDER=fast2sms      # production India (Fast2SMS.com)
SMS_PROVIDER=twilio        # international
FAST2SMS_API_KEY=your_key
```

---

## 🌐 Production Deployment

```bash
# Environment variables
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host/dbname
REDIS_URL=redis://localhost:6379/0
SMS_PROVIDER=fast2sms
FAST2SMS_API_KEY=your_key

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Run Celery (for SMS broadcasts)
celery -A config worker -l info
```

---

## 🎬 10-Minute Demo Script for Judges

1. **Admin panel** → show 8 workers, 3 contractors, 62 real engagements with ratings
2. **Login as Contractor** (9876540001) → Dashboard shows active jobs, stats, favourites
3. **Post urgent job** → "Mason needed today" with same-day flag → SMS broadcast fires
4. **Login as Worker** (9876543201 — Raju Sharma, mason) → See the urgent job card
5. **Apply in one tap** → No form, no CV, just one button
6. **Back as Contractor** → See applicant sorted by trust score, past work highlighted
7. **Click "Hire"** → Worker gets SMS confirmation
8. **Mark job complete** → Both parties confirm
9. **Rate each other** → Stars + one-line note, permanent after submit
10. **Contractor endorses** → "Reliable timekeeping", "Clean work" tagged to THIS job
11. **Worker profile** → Show timeline of completed jobs building up automatically
12. **Compare new vs. Raju** → New worker = honest empty slate; Raju = 20+ verified jobs

---

## 👥 Built By

20 senior full-stack engineers specializing in:
Django 5, DRF, PostgreSQL, Celery/Redis, PWA, Voice UI, Geolocation, SMS APIs

**For IIT Madras Hackathon 2025 — Web Development Domain**
