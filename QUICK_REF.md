# Quick Reference Card

## Admin Access
```
URL:      http://localhost:8000/admin/
Username: admin
Password: AdminPass123!
```

## Test User (Pre-created Example)
```
Username: student1
Password: TestPass123!
```

## Useful URLs
```
Home:         http://localhost:8000/
Olympiads:    http://localhost:8000/olympiads/
Chat:         http://localhost:8000/chat/room/general/
Leaderboard:  http://localhost:8000/profiles/scoreboard/
News:         http://localhost:8000/news/
```

## Commands
```
# Start server
.venv\Scripts\python manage.py runserver

# Run tests
.venv\Scripts\python manage.py test

# Check system
.venv\Scripts\python manage.py check

# Create superuser
.venv\Scripts\python manage.py createsuperuser

# Database operations
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py makemigrations
```

## Password Requirements
- Minimum 8 characters
- At least 1 UPPERCASE letter
- At least 1 digit (0-9)
- At least 1 special character (!@#$%^&* etc)

## Valid Test Passwords
- `MyPassword123!`
- `SecurePass@2024`
- `Test$Pass9`

