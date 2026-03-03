# School Olympiad Platform

Django + WebSocket platform for school olympiads with real-time chat, scoring, and auto-judging.

## Features

### Authentication & User Management
- Custom user model with admin/regular user roles
- Complex password validation (8+ chars, uppercase, digit, special char)
- Password reset flow via email (console backend in dev)
- User ban system for moderation

### Olympiad System
- Create olympiads by subject
- Questions with max scores
- Code/text submissions with auto-judging (Python)
- Cheating detection (duplicate code from same user)
- Automatic profile score updates

### Chat
- Real-time WebSocket chat by room
- Message persistence in DB
- Message deletion (soft delete)
- Ban checking prevents banned users from posting

### News/Announcements
- Rich text + image URL support
- Admin create/edit/delete
- Timestamped listings

### Profiles & Leaderboard
- User profile with bio, avatar link, score, rank
- Scoreboard sorted by score

### REST API
All endpoints at `/api/` (authentication required):
- `/api/users/` – user management
- `/api/olympiads/` – olympiad CRUD
- `/api/questions/` – questions
- `/api/submissions/` – code submissions + auto-grade
- `/api/chatmessages/` – chat history
- `/api/announcements/` – news
- `/api/profiles/` – user profiles

## Installation

```bash
# Setup virtualenv
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup DB
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Access:
- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`
- Home: `http://localhost:8000/`
- Chat: `http://localhost:8000/chat/<room>/`
- Scoreboard: `http://localhost:8000/profiles/scoreboard/`

## LAN Setup

To allow access from other machines on LAN (e.g., `192.168.10.214`):

1. Update `ALLOWED_HOSTS` in `school_platform/settings.py`
2. Start server: `python manage.py runserver 0.0.0.0:8000`
