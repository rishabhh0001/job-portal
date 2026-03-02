# JobPortal

A full-stack job portal built with Flask, inspired by the Naukri.com dark mode aesthetic. Supports three roles: job seekers, employers, and admins.

## Features

- **Job Seekers** — browse, search, filter, and apply for jobs. Track application status from a personal dashboard.
- **Employers** — post job listings, view applicants per job, and manage listings from a dashboard.
- **Admin** — platform overview with user, job, and application stats.
- Role-based access control, password hashing, and session management via Flask-Login.

## Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite (dev) / PostgreSQL (prod via `DATABASE_URL`)
- **Frontend:** HTML + Tailwind CSS (CDN)
- **Auth:** Flask-Login + Werkzeug password hashing

## Getting Started

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd job-portal

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed the database with sample data
python seed_data.py

# 5. Start the dev server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Test Accounts

| Role     | Email                   | Password     |
|----------|-------------------------|-------------|
| Seeker   | ravi@example.com        | password123 |
| Seeker   | priya@example.com       | password123 |
| Employer | hire@google.com         | password123 |
| Employer | hire@stripe.com         | password123 |
| Employer | hire@swiggy.in          | password123 |
| Admin    | admin@jobportal.com     | admin123    |

## Project Structure

```
job-portal/
├── app.py              # Routes and app factory
├── extensions.py       # SQLAlchemy db instance
├── models.py           # User, Job, Application models
├── config.py           # App config (secret key, DB URI)
├── seed_data.py        # Populates DB with sample data
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   ├── job_detail.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── dashboards/
│       ├── seeker.html
│       ├── employer.html
│       ├── post_job.html
│       ├── applications.html
│       └── admin.html
└── static/             # Custom CSS/JS if needed
```

## Environment Variables

| Variable       | Default                  | Description                |
|----------------|--------------------------|----------------------------|
| `SECRET_KEY`   | `scrt_key-@jbportal11`   | Flask session signing key  |
| `DATABASE_URL` | `sqlite:///jobportal.db` | SQLAlchemy database URI    |

For production, set these in a `.env` file or your hosting environment.
