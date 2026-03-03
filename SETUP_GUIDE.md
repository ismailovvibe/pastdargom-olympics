# School Olympiad Platform - Setup & Usage Guide

## System Overview

**School Olympiad Platform** is a Django-based web application for managing programming olympiads and competitions. It features real-time chat, automatic code grading, multiple-choice questions, scoring systems, and comprehensive admin management.

### Technology Stack
- **Backend:** Django 6.0.2 + Django REST Framework 3.16.1
- **Real-time:** Django Channels 4.3.2 (WebSocket chat)
- **Database:** SQLite (development)
- **Frontend:** HTML5 + Tailwind CSS 3
- **Authentication:** Django custom User model with role-based access

---

## ADMIN SETUP

### Admin Credentials
```
Username: admin
Password: AdminPass123!
Email:    admin@olympiad.local
```

### Accessing Admin Panel
1. Start the development server (see "Running the Application" below)
2. Navigate to: `http://localhost:8000/admin/`
3. Login with credentials above
4. You'll see the admin dashboard with all management options

### Admin Panel Features

#### Users Management (`/admin/users/student/`)
- **Create New User**: Click "Add Student"
  - Username: unique identifier (e.g., `student1`)
  - Email: valid email address
  - Password: must meet requirements (8+ chars, uppercase, digit, special char)
  - Is Admin: check box to grant staff access
  - Is Banned: check box to ban user from chat
- **Edit User**: Click username to modify details
- **Ban User**: Check "Is Banned" to prevent chat access
- **Delete User**: Click delete button to remove account

#### Olympiad Management (`/admin/olympiads/olympiad/`)
- **Create Olympiad**: Click "Add Olympiad"
  - Name: competition title (e.g., "Python Fundamentals 2024")
  - Description: detailed description
  - Status: Choose from PENDING / ACTIVE / COMPLETED
  - Duration Minutes: time limit per attempt (e.g., 120 for 2 hours)
  - Max Score: total possible points
- **Add Questions**: In olympiad page, scroll to "Questions" section
  - Click "Add another Question"
  - Question: the problem statement
  - Question Type: TEXT / CODE / MC (multiple choice)
  - Max Score: points for this question
  - Hint: optional guidance for participants
  - For MC questions: enter options and correct answer

#### View Submissions (`/admin/olympiads/submission/`)
- See all user submissions with timestamps
- View submission content and auto-detected cheating flags
- Filter by user or olympiad

#### Monitor Chat Messages (`/admin/chat/chatmessage/`)
- View all chat messages
- Delete inappropriate messages
- See message timestamps and authors

#### Announcements (`/admin/news/announcement/`)
- Create announcements visible to all users
- Add images via URL
- Edit and delete announcements

#### User Profiles & Scores (`/admin/profiles/profile/`)
- View user scores and rankings
- View user bios
- See profile statistics

### Admin Bulk Actions
- Select multiple items using checkboxes
- Use "Action" dropdown to apply bulk operations:
  - Delete selected items
  - Ban/unban users
  - Change olympiad status

---

## USER SETUP & REGISTRATION

### Creating a New User Account

#### Option 1: Web Registration
1. Navigate to: `http://localhost:8000/auth/register/`
2. Fill in registration form:
   - **Username**: Unique identifier (3-30 characters, letters/numbers/underscore)
   - **Email**: Valid email address
   - **Password**: Must meet requirements:
     - Minimum 8 characters
     - At least one uppercase letter (A-Z)
     - At least one digit (0-9)
     - At least one special character (!@#$%^&*, etc.)
   - **Confirm Password**: Re-enter password
3. Click "Register"
4. You'll be redirected to login page

#### Example Valid Passwords
- `MyPass123!`
- `Secure@Pass9`
- `Strong$2024Pwd`
- `Abc123!xyz`

#### Invalid Password Examples (will be rejected)
- `simple` - no uppercase, no digit, no special char
- `Password123` - no special character
- `Pass1!` - less than 8 characters
- `mypassword1!` - no uppercase letters

#### Option 2: Admin Creates User
1. Login to admin panel
2. Navigate to Users section
3. Click "Add Student"
4. Fill in details and set password
5. User can change password after first login

### Login
1. Navigate to: `http://localhost:8000/auth/login/`
2. Enter username and password
3. Click "Login"
4. You'll be redirected to olympiad list

---

## USER FEATURES

### Participating in Olympiad
1. After login, go to "Olimpiadalar" (Olympiads)
2. Click on active olympiad to view questions
3. For each question:
   - **TEXT submissions**: Type answer in text box, click "Submit"
   - **CODE submissions**: Write Python code, click "Submit"
   - **MC (Multiple Choice)**: Select one radio button option, click "Submit"
4. See result: points earned, percentage correct
5. Attempt tracking: track how many times you solved each problem

### Key Features
- **Attempt Limit**: You can attempt each question multiple times
- **Hints**: Optional hints available for each question
- **Timer**: Olympiad has duration limit
- **Cheating Detection**: System auto-detects code copied from templates
- **Real-time Chat**: Chat room accessible from navigation

### Real-time Chat
1. Click "Leaderboard" → join chat room
2. Type message and press Enter
3. Messages appear instantly for all users in room
4. If you're banned by admin, chat will be blocked

### Leaderboard
1. Click "Leaderboard" in navigation
2. View all users ranked by score
3. See your position in standings
4. Scores update in real-time

### Profile
1. Click "Profile" in navigation
2. View your score and position
3. Edit bio and avatar (currently avatar via URL)

### Announcements
1. Click "Elonlar" (Announcements)
2. View all news and updates from admin
3. Announcements include images and descriptions

---

## RUNNING THE APPLICATION

### Prerequisites
- Python 3.14+
- Virtual environment activated
- All dependencies installed

### Start Development Server
```bash
cd c:\Users\P2IMI11\Desktop\School
python manage.py runserver
```

Server will start at: `http://localhost:8000/`

### For LAN Access (Local Network)
```bash
python manage.py runserver 0.0.0.0:8000
```

Then access from other computers on LAN:
- Replace `localhost` with your computer's IP address
- Example: `http://192.168.1.100:8000/`

### Stop Server
Press `Ctrl+C` in terminal

---

## KEY URLS & PAGES

| Page | URL | Access |
|------|-----|--------|
| Home | `/` | All |
| Register | `/auth/register/` | Anonymous |
| Login | `/auth/login/` | Anonymous |
| Logout | `/auth/logout/` | Authenticated |
| Olympiads List | `/olympiads/` | Authenticated |
| Question Detail | `/olympiads/<id>/` | Authenticated |
| Leaderboard | `/profiles/scoreboard/` | All |
| User Profile | `/profiles/` | Authenticated |
| Announcements | `/news/` | All |
| Admin Panel | `/admin/` | Staff only |
| Chat Room | `/chat/room/<name>/` | Authenticated |

---

## API ENDPOINTS (for developers)

All endpoints require authentication (session or JWT token)

### Users API
```
GET/POST   /api/users/
GET/PUT    /api/users/<id>/
```

### Olympiads API
```
GET/POST   /api/olympiads/
GET/PUT    /api/olympiads/<id>/
GET/POST   /api/questions/
GET/PUT    /api/questions/<id>/
GET/POST   /api/submissions/
GET/PUT    /api/submissions/<id>/
```

### Profiles API
```
GET/POST   /api/profiles/
GET        /api/profiles/scoreboard/
```

### Chat API
```
GET/POST   /api/chatmessages/
DELETE     /api/chatmessages/<id>/
```

### News API
```
GET/POST   /api/announcements/
GET/PUT    /api/announcements/<id>/
```

---

## TROUBLESHOOTING

### Issue: "Port 8000 already in use"
**Solution:** 
```bash
python manage.py runserver 8001
# or kill existing process and restart
```

### Issue: "Database error" on first run
**Solution:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Issue: "Static files not loading" (CSS/images)
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: "Chat not connecting"
**Solution:**
- Ensure you're authenticated (logged in)
- Check WebSocket connection in browser console
- Restart development server

### Issue: "Can't upload images"
**Solution:**
- Currently images are URL-based only
- Use external URL or image hosting service
- Update profile/olympiad with image URL

---

## DATABASE OPERATIONS

### Backup Database
```bash
copy db.sqlite3 db.sqlite3.backup
```

### Reset Database (WARNING: deletes all data)
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### View Database
```bash
python manage.py dbshell
```

---

## TESTING

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test Module
```bash
python manage.py test users.tests
python manage.py test olympiads.tests
python manage.py test chat.tests
```

### Expected Output
```
Ran 19 tests in X.XXXs

OK
```

---

## PROJECT STRUCTURE

```
school_platform/
├── users/            # User authentication & management
│   ├── models.py     # Custom User model
│   ├── views.py      # Login, register, logout
│   ├── forms.py      # Custom user form with password validator
│   └── templates/    # Auth UI (login, register, password reset)
│
├── olympiads/        # Competition management
│   ├── models.py     # Olympiad, Question, Submission
│   ├── views.py      # Olympiad list, question detail, submission
│   └── templates/    # Olympiad UI
│
├── profiles/         # User profiles & leaderboard
│   ├── models.py     # Profile model
│   ├── views.py      # Profile detail, scoreboard
│   └── templates/    # Profile UI
│
├── chat/             # Real-time messaging
│   ├── models.py     # ChatMessage model
│   ├── consumers.py  # WebSocket consumer
│   └── routing.py    # WebSocket routing
│
├── news/             # Announcements
│   ├── models.py     # Announcement model
│   └── views.py      # News list
│
├── school_platform/ # Project settings
│   ├── settings.py   # Django configuration
│   ├── urls.py       # URL routing
│   ├── asgi.py       # ASGI for WebSocket
│   └── wsgi.py       # WSGI for HTTP
│
├── templates/        # Base template (layout)
├── static/           # CSS, JS, images
├── db.sqlite3        # Database file
└── manage.py         # Django management script
```

---

## PERFORMANCE TIPS

1. **For 100+ users**: Switch to PostgreSQL database
2. **For real-time features**: Deploy with Daphne + Channels
3. **For file uploads**: Configure S3 or similar storage
4. **For email**: Setup real SMTP backend in settings.py
5. **For scaling**: Use Redis for caching and WebSocket layer

---

## SECURITY NOTES

- Change admin password immediately in production
- Use HTTPS in production (not just HTTP)
- Set DEBUG=False in production settings
- Use strong SECRET_KEY in production
- Don't commit db.sqlite3 to version control
- Use environment variables for sensitive data

---

## SUPPORT & LICENSE

**Created:** 2024 School Olympiad Platform
**Framework:** Django 6.0.2
**Python:** 3.14

For issues or questions, review Django documentation at https://docs.djangoproject.com/

