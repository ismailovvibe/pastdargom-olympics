# SYSTEM ARCHITECTURE OVERVIEW

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────┐  ┌─────────────────────────────────┐  │
│  │   HTML Templates     │  │   WebSocket Client (Chat)       │  │
│  │  - base.html         │  │   - Real-time messaging          │  │
│  │  - auth/*.html       │  │   - Message persistence          │  │
│  │  - olympiad/*.html   │  │   - Ban enforcement              │  │
│  │  - profile/*.html    │  │                                  │  │
│  │  (Tailwind CSS)      │  │                                  │  │
│  └──────────────────────┘  └─────────────────────────────────┘  │
│                                                                   │
└─────────────────┬──────────────────────────────────┬─────────────┘
                  │                                  │
           HTTP Requests                    WebSocket Connection
                  │                                  │
┌─────────────────▼──────────────────────────────────▼─────────────┐
│                      DJANGO FRAMEWORK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         URL Router (urls.py)                             │    │
│  │  ├─ /admin/          → Django Admin                      │    │
│  │  ├─ /auth/           → Authentication                    │    │
│  │  ├─ /olympiads/      → Olympiad Views                    │    │
│  │  ├─ /chat/           → Chat Views                        │    │
│  │  ├─ /news/           → News Views                        │    │
│  │  ├─ /profiles/       → Profile Views                     │    │
│  │  ├─ /api/            → REST API (DefaultRouter)          │    │
│  │  └─ ws/chat/*/       → WebSocket (Channels)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              APPLICATION LAYER (5 Apps)                │     │
│  │                                                        │     │
│  │  USERS App                                            │     │
│  │  ├─ Models: CustomUser (AbstractUser extension)       │     │
│  │  ├─ Forms: CustomUserCreationForm + Password Val      │     │
│  │  ├─ Views: LoginView, RegisterView, LogoutView        │     │
│  │  ├─ Validators: ComplexPasswordValidator              │     │
│  │  └─ Serializers: UserSerializer, UserDetailSerializer │     │
│  │                                                        │     │
│  │  OLYMPIADS App                                        │     │
│  │  ├─ Models:                                           │     │
│  │  │  - Olympiad (competition container)                │     │
│  │  │  - Question (3 types: TEXT/CODE/MC)                │     │
│  │  │  - Submission (user attempts)                      │     │
│  │  ├─ Views: Question Detail, Submission Result         │     │
│  │  ├─ ViewSets: OlympiadViewSet, QuestionViewSet        │     │
│  │  │  └─ SubmissionViewSet (auto-scoring logic)         │     │
│  │  ├─ Logic:                                            │     │
│  │  │  - MC evaluation: instant correct/wrong            │     │
│  │  │  - Code grading: "print(" detection                │     │
│  │  │  - Cheating detection: code similarity flagging    │     │
│  │  │  - Attempt tracking: counts per question           │     │
│  │  └─ Scoring: auto-increment Profile.score on submit   │     │
│  │                                                        │     │
│  │  CHAT App                                             │     │
│  │  ├─ Models: ChatMessage (with soft-delete)            │     │
│  │  ├─ Consumers: ChatConsumer (WebSocket handler)       │     │
│  │  ├─ Routing: WebSocket URL patterns                   │     │
│  │  ├─ Logic:                                            │     │
│  │  │  - Message persistence in DB                       │     │
│  │  │  - Ban enforcement on connection                   │     │
│  │  │  - Real-time broadcast to group                    │     │
│  │  └─ Serializers: ChatMessageSerializer                │     │
│  │                                                        │     │
│  │  PROFILES App                                         │     │
│  │  ├─ Models: Profile (OneToOne with User)              │     │
│  │  ├─ Views: Scoreboard, Profile Detail                 │     │
│  │  ├─ ViewSets: ProfileViewSet                          │     │
│  │  ├─ Signals: auto-create Profile on User creation     │     │
│  │  └─ Scoring: updated by Submission logic              │     │
│  │                                                        │     │
│  │  NEWS App                                             │     │
│  │  ├─ Models: Announcement (news/updates)               │     │
│  │  ├─ Views: News List                                  │     │
│  │  ├─ ViewSets: AnnouncementViewSet                     │     │
│  │  └─ Serializers: AnnouncementSerializer               │     │
│  │                                                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────┐  ┌────────────────────────┐  │
│  │   REST Framework             │  │   Channels (ASGI)      │  │
│  │   - DefaultRouter            │  │   - ProtocolTypeRouter │  │
│  │   - ViewSets (CRUD)          │  │   - WebSocket support  │  │
│  │   - Serializers              │  │   - In-memory layer    │  │
│  │   - Authentication (Session) │  │                        │  │
│  └──────────────────────────────┘  └────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │        Authentication & Authorization                    │    │
│  │  ├─ Django built-in auth: login, logout, permissions    │    │
│  │  ├─ Custom User model with is_admin, is_banned flags    │    │
│  │  ├─ Password validation: 8+ chars, uppercase, digit     │    │
│  │  ├─ Session-based (development)                         │    │
│  │  └─ JWT-ready architecture (for future)                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────┬──────────────────────────────────┬─────────────┘
                  │                                  │
             SQL Queries                   WebSocket Messages
                  │                                  │
┌─────────────────▼──────────────────────────────────▼─────────────┐
│                      DATABASE LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  SQLite (Development)  →  PostgreSQL (Production)                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Tables:                                                   │   │
│  │  - auth_user (Django built-in)                          │   │
│  │  - users_student (Custom User model)                    │   │
│  │  - olympiads_olympiad                                    │   │
│  │  - olympiads_question                                    │   │
│  │  - olympiads_submission                                  │   │
│  │  - chat_chatmessage                                      │   │
│  │  - profiles_profile                                      │   │
│  │  - news_announcement                                     │   │
│  │  - auth_group (for permissions)                          │   │
│  │  - auth_permission (permissions)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Key Relationships:                                        │   │
│  │  User ──1:1─→ Profile (scoring)                          │   │
│  │  User ──1:Many─→ Submission (attempts)                   │   │
│  │  User ──1:Many─→ ChatMessage                             │   │
│  │  Olympiad ──1:Many─→ Question                            │   │
│  │  Question ──1:Many─→ Submission                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### User Registration & Login Flow

```
┌──────────────┐
│ User visits  │
│ /register/   │
└────────┬─────┘
         │
         ▼
┌──────────────────────────────┐
│ Registration Form            │
│ - Username (unique)          │
│ - Email                      │
│ - Password (validated)       │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ ComplexPasswordValidator     │
│ ✓ 8+ chars                   │
│ ✓ Uppercase letter           │
│ ✓ Digit                      │
│ ✓ Special character          │
└────────┬─────────────────────┘
         │
    Valid?
    /    \
   Yes    No
   │       │
   ▼       └─→ Error message
┌──────────────────────────────┐
│ Create User                  │
│ - Hash password (PBKDF2)     │
│ - Store in database          │
│ - Create Profile (OneToOne)  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Redirect to /login/          │
│ User enters credentials      │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Authenticate                 │
│ - Username lookup            │
│ - Password verification      │
│ - Store session              │
└────────┬─────────────────────┘
         │
    Valid?
   /    \
  Yes    No
  │       │
  ▼       └─→ "Invalid credentials"
┌──────────────────────────────┐
│ Set session cookie           │
│ Redirect to /olympiads/      │
└──────────────────────────────┘
```

### Olympiad Submission & Scoring Flow

```
┌─────────────────────────────┐
│ User Views Question          │
│ - Question detail page       │
│ - Display question type      │
│ - Show hint (if available)   │
└────────┬────────────────────┘
         │
         ▼
    Question Type?
    ├─ TEXT
    ├─ CODE
    └─ MC
         │
    ┌────┴────┬────────┬───────┐
    ▼         ▼        ▼       ▼
  TEXT      CODE      MC    Default
    │         │        │
    ▼         ▼        ▼
  Textarea  textarea  Radio
  with      with      buttons
  multi-    Python    (select
  line      syntax    one op)
    │        hint     │
    └────┬────┘       │
         │            │
         ▼            ▼
    ┌──────────────────────────────┐
    │ User Submits Response        │
    │ - POST to /olympiads/<id>/   │
    │ - Capture response text      │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Scoring Logic                │
    │ (SubmissionViewSet.perform)  │
    └────────┬─────────────────────┘
             │
        Question Type?
        /    |    \
    TEXT   CODE    MC
      │      │      │
      ▼      ▼      ▼
    Accept Check   Compare
    any    for     to
    text   "print" mc_answer
      │      │      │
      ▼      ▼      ▼
    points  ✓/✗    ✓/✗
      │      │      │
    └───┬────┘      │
        │           │
        └─────┬─────┘
              ▼
    ┌──────────────────────────────┐
    │ Update Profile Score         │
    │ - Increment score by points  │
    │ - Recalculate rank           │
    │ - Broadcast leaderboard      │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Store Submission             │
    │ - Record attempt number      │
    │ - Save response text         │
    │ - Flag cheating (if detected)│
    │ - Timestamp submission       │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Display Result               │
    │ - Points earned              │
    │ - Percentage correct         │
    │ - Attempt number             │
    │ - Option to retry            │
    └──────────────────────────────┘
```

### Chat Message Flow (WebSocket)

```
┌──────────────────────────────┐
│ User Navigates to Chat       │
│ /chat/room/general/          │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ WebSocket Connection         │
│ (ChatConsumer.connect)       │
└────────┬─────────────────────┘
         │
         ▼
    Check if user banned?
    /              \
   Yes             No
    │               │
    ▼               ▼
 Reject       Add to group
 Connection   "chat_general"
   │               │
   └────────┬──────┘
            │
            ▼
    ┌──────────────────────────────┐
    │ User Types Message           │
    │ - Input field                │
    │ - Press Enter/Send           │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ WebSocket Message Received   │
    │ (ChatConsumer.receive)       │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Check: User still not banned?│
    │ Is message valid?            │
    └────────┬─────────────────────┘
             │
       ┌─────┴─────┐
       ▼           ▼
     OK         REJECT
      │           │
      ▼           └─→ Send error
    ┌──────────────────────────────┐
    │ Save ChatMessage to DB       │
    │ - room_name: "general"       │
    │ - user: current_user         │
    │ - message: text              │
    │ - timestamp: now()           │
    │ - deleted: False             │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Broadcast to Chat Group      │
    │ Using channels.layers        │
    │ - Send to all connected WS   │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ All Clients Receive Message  │
    │ (WebSocket.receive event)    │
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │ Display Message in Chat UI   │
    │ - Author: username           │
    │ - Content: message text      │
    │ - Timestamp                  │
    │ - Animate slide-up           │
    └──────────────────────────────┘
```

---

## Request/Response Cycle

### Web Request (HTTP)

```
USER ACTION
    │
    ▼
┌─────────────────────┐
│ Browser HTTP Request│
│ GET /olympiads/1/   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Django URL Router (urls.py)             │
│ - Match URL pattern                     │
│ - Extract parameters (id=1)             │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Authentication Middleware               │
│ - Check session cookie                  │
│ - Load user object                      │
│ - Set request.user                      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ View/ViewSet Handler                    │
│ - olympiad = get_object_or_404(id)      │
│ - questions = olympiad.question_set.all │
│ - Prepare context data                  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Template Rendering                      │
│ - Load template (question_detail.html)  │
│ - Render with context data              │
│ - Generate HTML                         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ HTTP Response                           │
│ Status: 200 OK                          │
│ Content-Type: text/html                 │
│ Body: HTML page                         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Browser Receives Response               │
│ - Parse HTML                            │
│ - Load CSS (Tailwind)                   │
│ - Execute JS                            │
│ - Trigger animations                    │
│ - Display page to user                  │
└─────────────────────────────────────────┘
```

### API Request (REST)

```
JAVASCRIPT FETCH
    │
    ▼
┌──────────────────────────────┐
│ AJAX HTTP Request            │
│ GET /api/olympiads/          │
│ Accept: application/json     │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ DefaultRouter Dispatch       │
│ - Match /api/olympiads/      │
│ - OlympiadViewSet.list()     │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ IsAuthenticated Permission   │
│ - Check request.user         │
│ - Allow if authenticated     │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ ViewSet Handler              │
│ - queryset.all()             │
│ - OlympiadSerializer()       │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ JSON Serialization           │
│ - Convert objects to dicts   │
│ - Serialize nested relations │
│ - Generate JSON              │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ HTTP Response                │
│ Status: 200 OK               │
│ Content-Type: application/   │
│ json                         │
│ Body: [{"id": 1, ...}, ...]  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ JavaScript Receives JSON     │
│ - Parse JSON response        │
│ - Update UI with data        │
│ - Trigger callbacks          │
└──────────────────────────────┘
```

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────┐
│ Production Environment                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────┐                   │
│  │ Nginx (Reverse Proxy)       │                   │
│  │ - Load balancing            │                   │
│  │ - SSL termination           │                   │
│  │ - Static files serving      │                   │
│  │ - Request routing           │                   │
│  └───────────┬─────────────────┘                   │
│              │                                     │
│      ┌───────┴──────────┐                          │
│      │                  │                          │
│      ▼                  ▼                          │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Daphne ASGI │  │ Daphne ASGI  │ (x2 instances)│
│  │ Server 1    │  │ Server 2     │               │
│  │ :8001       │  │ :8002        │               │
│  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                       │
│         └────────┬────────┘                        │
│                  │                                │
│                  ▼                                │
│        ┌──────────────────────────┐               │
│        │ PostgreSQL Database      │               │
│        │ - Persistent data        │               │
│        │ - Connection pooling     │               │
│        │ - Automatic backups      │               │
│        └──────────────────────────┘               │
│                  │                                │
│        ┌─────────┴──────────┐                     │
│        ▼                    ▼                     │
│     ┌──────────┐      ┌──────────┐               │
│     │ Redis    │      │ Redis    │ (Persist)    │
│     │ Cache    │      │ Channels │               │
│     │ Server   │      │ Layer    │               │
│     └──────────┘      └──────────┘               │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │ Celery Task Queue (Background Jobs)         │  │
│  │ - Code evaluation                          │  │
│  │ - Email sending                            │  │
│  │ - Report generation                        │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## Performance Optimization Areas

| Component | Current | Production |
|-----------|---------|-----------|
| Database | SQLite | PostgreSQL + connection pooling |
| Cache | None | Redis (session, query cache) |
| WebSocket | In-memory | Redis layer |
| Static Files | Served by Django | Nginx/S3 |
| Async Tasks | Blocking | Celery + RabbitMQ |
| Monitoring | Console logs | ELK Stack/Datadog |
| Security | HTTP | HTTPS/SSL |

