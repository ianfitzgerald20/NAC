# BulldogConnect — Norfolk Academy

AcademyConnect is an alumni-student networking platform for Norfolk Academy. It connects students with alumni mentors for career guidance, job postings, and direct messaging.

---

## Project Structure

```
BulldogConnect/
├── frontend/
│   ├── pages/
│   │   ├── index.html        # Landing page
│   │   └── app.html          # Main application (SPA with 8 views)
│   └── assets/
│       └── images/           # Logos and images
├── backend/
│   ├── app.py                # Flask server (serves frontend + REST API)
│   ├── requirements.txt
│   ├── routes/
│   │   ├── alumni.py         # GET /api/alumni, GET /api/alumni/:id
│   │   ├── jobs.py           # GET /api/jobs, GET /api/jobs/:id
│   │   └── auth.py           # POST /api/auth/login, /api/auth/register
│   └── data/
│       ├── alumni.json       # Alumni seed data
│       └── jobs.json         # Job/internship seed data
└── .claude/
    └── launch.json           # Dev server configuration
```

---

## Pages (inside app.html)

| View | Description |
|------|-------------|
| Home / Directory | Browse and filter alumni by industry, college, availability |
| Profile | Alumni profile with Overview, Career Timeline, and Book a Session tabs |
| Messages | Direct messaging threads between students and alumni |
| Jobs | Job and internship board — alumni post, students browse |
| Admin | Dashboard with stats, activity feed, and user management |
| My Profile | Edit student or alumni profile |
| Student Onboarding | 4-step flow: interests → mentoring format → matched mentors |
| Alumni Registration | 4-step flow: info → LinkedIn → expertise/availability → preview |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alumni` | List all alumni (filter: `?industry=`, `?availability=`) |
| GET | `/api/alumni/:id` | Get a single alumni profile |
| GET | `/api/jobs` | List all jobs (filter: `?industry=`, `?type=`) |
| GET | `/api/jobs/:id` | Get a single job posting |
| POST | `/api/auth/login` | Login (returns stub token) |
| POST | `/api/auth/register` | Register new user |

---

## Getting Started

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the server

```bash
python backend/app.py
```

Or use the Claude Code dev server (`.claude/launch.json`).

The Flask server serves both the frontend pages and the REST API on the same port (default: **8081**).

- Landing page: http://localhost:8081/
- App (student): http://localhost:8081/app?role=student
- App (alumni): http://localhost:8081/app?role=alumni

---

## Role-Based Access

The app switches between two views via a URL parameter:

- `?role=student` — Browse alumni directory, apply to jobs, message mentors
- `?role=alumni` — Post jobs, manage availability, respond to students
