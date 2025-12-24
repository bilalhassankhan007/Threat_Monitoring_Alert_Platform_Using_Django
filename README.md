***THREAT MONITORING & ALERT MANAGEMENT PLATFORM***  
***Django + Django REST Framework + JWT + Swagger + PostgreSQL***

![Python](https://img.shields.io/badge/Python-3.x-blue)  
![Django](https://img.shields.io/badge/Django-5.x-green)  
![DRF](https://img.shields.io/badge/DRF-3.x-red)  
![JWT](https://img.shields.io/badge/Auth-JWT-orange)  
![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-blue)  
![Swagger](https://img.shields.io/badge/Docs-Swagger%20(OpenAPI)-brightgreen)  

---

#### ***TABLE OF CONTENTS***
- ***1) Problem Statement***
- ***2) Objective***
- ***3) Approach***
- ***4) Project Overview***
- ***5) Technology Stack***
- ***6) Project Structure***
- ***7) Folder-by-Folder Explanation***
- ***8) File-by-File Summary***
- ***9) Execution Flow (Startup → Request → Response)***
- ***10) API Endpoints***
- ***11) Architecture + Diagrams***
  - Architecture Diagram
  - Sequence Diagram
  - ER Diagram
- ***12) Setup & Configuration (Windows 11 + VS Code)***
- ***13) Deployment (Render, No Docker)***
- ***14) Developer Notes (Extend / Debug / Maintain)***
- ***15) Conclusion***

---

#### ***1) PROBLEM STATEMENT***
The goal is to build a backend service that ingests security events from multiple sources and exposes secure REST APIs for managing and viewing alerts.  
This backend is designed as a foundation that can later integrate with systems like:

- Surveillance Systems  
- SIEM Tools  
- AI-based Threat Detectors  

---

#### ***2) OBJECTIVE***
Build a backend API system using ***Django + DRF*** that supports:

- Secure user authentication (JWT or Django auth)
- Roles → ***Admin*** and ***Analyst***
- Threat/Event ingestion and storage in database
- Automatic alert generation on HIGH/CRITICAL events
- Alert listing, filtering, pagination
- Admin-only status updates
- Swagger API docs (bonus)
- Rate limiting + logging + tests (bonus)

---

#### ***3) APPROACH***
***Architecture Approach →***
- Build clean Django apps with separation of concerns  
  - `accounts/` → users + roles  
  - `monitoring/` → events + alerts + APIs + dashboard utilities  

***Security Approach →***
- JWT tokens using `simplejwt`
- DRF permissions enforcing RBAC
- Input validation via DRF serializers
- Avoid sensitive data exposure in responses

***Data Approach →***
- PostgreSQL as primary DB
- SQLite as fallback for local/dev (if Postgres not configured)
- Proper indexing for frequently filtered fields (severity, status, timestamps)
- Query optimization using `select_related()` to avoid N+1

***Demo Approach →***
- Provide Swagger for API testing
- Provide a dashboard page to demonstrate everything in one place:
  - Swagger link
  - Admin link
  - JWT token generator
  - Admin tools (create analyst, test critical event)
  - Alerts list/filter/update

---

#### ***4) PROJECT OVERVIEW***
This project provides:

- ***JWT Authentication***
  - Generate access/refresh tokens
  - Use `Authorization: Bearer <token>`

- ***Role-Based Access Control***
  - Admin → full access
  - Analyst → read-only for alerts

- ***Event Ingestion***
  - POST event with source_name, event_type, severity, description
  - timestamp generated automatically

- ***Auto Alert Generation***
  - If severity HIGH or CRITICAL → create alert automatically

- ***Alert Management***
  - List + filter by severity/status
  - Pagination enabled
  - Admin-only update alert status

- ***Swagger Documentation***
  - `/api/docs/`

- ***Dashboard Demo UI***
  - `/` root page

---

#### ***5) TECHNOLOGY STACK***

***Languages →***
- Python  
- HTML + CSS + JavaScript (Dashboard)

***Frameworks / Libraries →***
- Django  
- Django REST Framework  
- JWT Auth → `djangorestframework-simplejwt`  
- Filtering → `django-filter`  
- Swagger/OpenAPI → `drf-spectacular`  
- Env config → `python-dotenv`  
- DB parsing → `dj-database-url`  
- Static handling → `whitenoise`  
- Production server → `gunicorn`  

***Databases →***
- PostgreSQL (primary)
- SQLite (local fallback if Postgres not configured)

---

#### ***6) PROJECT STRUCTURE (TREE)***


threat-platform/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ build.sh
├─ render.yaml (optional)
├─ db.sqlite3 (local fallback)
│
├─ threat_platform/
│ ├─ settings.py
│ ├─ urls.py
│ ├─ asgi.py
│ └─ wsgi.py
│
├─ accounts/
│ ├─ models.py
│ ├─ admin.py
│ ├─ apps.py
│ └─ migrations/
│
└─ monitoring/
├─ models.py
├─ serializers.py
├─ permissions.py
├─ filters.py
├─ views.py
├─ signals.py
├─ dashboard_api.py
├─ urls.py
├─ pagination.py
├─ tests.py
├─ migrations/
└─ templates/
└─ monitoring/
└─ dashboard.html

#### ***7) FOLDER-BY-FOLDER EXPLANATION***

***threat_platform/***  
- Global Django settings and routes  
- JWT setup + Swagger endpoints  
- DB configuration  

***accounts/***  
- Custom user model with role support  
- Supports ADMIN / ANALYST roles  
- Used by DRF permissions  

***monitoring/***  
- Implements domain logic:
  - Event model
  - Alert model
  - Auto alert generation
  - REST APIs
  - Dashboard helper APIs

***templates/***  
- Dashboard UI (single page demo hub)

---

#### ***8) FILE-BY-FILE SUMMARY (KEY FILES)***

***manage.py***  
- Django command line entry point  
- Runs server, migrations, createsuperuser, etc.  

***threat_platform/settings.py***  
- Loads `.env`
- Configures DRF, JWT, Swagger
- Configures database via `DATABASE_URL`  
- Sets static config for WhiteNoise  

***threat_platform/urls.py***  
- Routes:
  - `/` dashboard
  - `/admin/`
  - `/api/`
  - `/api/auth/token/`
  - `/api/docs/`

***accounts/models.py***  
- Custom `User(AbstractUser)`  
- Adds `role` field  
- Adds `is_admin_role` property  

***monitoring/models.py***  
- Defines `Event` and `Alert` models  

***monitoring/signals.py***  
- Auto-creates alert on HIGH/CRITICAL events  

***monitoring/serializers.py***  
- Input validation + clean output formatting  

***monitoring/permissions.py***  
- RBAC enforcement:
  - Admin → write access  
  - Analyst → read-only alerts  

***monitoring/views.py***  
- DRF ViewSets for events/alerts  
- Uses query optimization `select_related()`  

***monitoring/dashboard_api.py***  
- Dashboard helper APIs:
  - Create analyst (admin only)
  - Test critical event (admin only)
  - List alerts with filters (admin/analyst)
  - Update alert status (admin only)

***monitoring/templates/monitoring/dashboard.html***  
- Demo UI to show everything from one page  

---

#### ***9) EXECUTION FLOW (STARTUP → REQUEST → RESPONSE)***

***Startup Flow →***
- `python manage.py runserver`
- Django loads settings
- Apps load (accounts, monitoring)
- URL router registers endpoints
- Dashboard available at `/`

***JWT Flow →***
- POST `/api/auth/token/` with username/password
- Server returns access + refresh token
- Client sends token in header:
  - `Authorization: Bearer <access_token>`

***Event Ingestion Flow →***
- Admin sends POST `/api/events/`
- Serializer validates data
- Event saved to DB
- Signal triggers:
  - if HIGH/CRITICAL → create alert
- Response returned (201 Created)

***Alert Flow →***
- GET `/api/alerts/` with optional filters:
  - `?severity=CRITICAL`
  - `?status=OPEN`
- Pagination applied
- Admin can PATCH update status

---

#### ***10) API ENDPOINTS (SUMMARY)***

***Auth →***
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `POST /api/auth/token/verify/`

***Events →***
- `POST /api/events/` (Admin)
- `GET /api/events/` (optional depending on permissions)

***Alerts →***
- `GET /api/alerts/` (Admin + Analyst)
- `PATCH /api/alerts/<id>/` (Admin only)

***Dashboard Helpers →***
- `POST /api/dashboard/create-analyst/` (Admin only)
- `POST /api/dashboard/test-api/` (Admin only)
- `GET /api/dashboard/alerts/` (Admin + Analyst)
- `PATCH /api/dashboard/alerts/<id>/status/` (Admin only)

***Docs →***
- `/api/schema/`
- `/api/docs/`

---

#### ***11) ARCHITECTURE + DIAGRAMS***

***11.1 Architecture Diagram***
```mermaid
flowchart LR
  UI[Dashboard UI] --> AUTH[JWT Auth]
  Swagger[Swagger UI] --> API[DRF API Layer]
  UI --> API
  API --> DB[(PostgreSQL)]
  API --> SIG[Signals/Rules]
  SIG --> DB

11.2 Sequence Diagram (Event → Auto Alert)
sequenceDiagram
  participant C as Client
  participant A as DRF API
  participant DB as Database
  participant S as Signal/Rule

  C->>A: POST /api/events/ (severity=CRITICAL)
  A->>DB: INSERT Event
  DB-->>A: Event saved
  A->>S: post_save(Event)
  S->>DB: INSERT Alert(status=OPEN)
  DB-->>S: Alert saved
  A-->>C: 201 Created


11.3 ER Diagram (Entities)
erDiagram
  USER ||--o{ EVENT : creates
  EVENT ||--|| ALERT : generates

  USER {
    int id
    string username
    string role
  }

  EVENT {
    int id
    string source_name
    string event_type
    string severity
    string description
    datetime timestamp
  }

  ALERT {
    int id
    string status
    datetime created_at
    int event_id
  }

12) SETUP & CONFIGURATION (WINDOWS 11 + VS CODE)
Step 1 → Create and Activate Virtual Env
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Step 2 → Install Dependencies
pip install -r requirements.txt

Step 3 → Create .env
copy .env.example .env

Step 4 → Run Migrations
python manage.py makemigrations
python manage.py migrate

Step 5 → Create Admin User
python manage.py createsuperuser

Step 6 → Run Server
python manage.py runserver


Important URLs →

Dashboard → http://127.0.0.1:8000/
Swagger → http://127.0.0.1:8000/api/docs/
Admin → http://127.0.0.1:8000/admin/


13) DEPLOYMENT (RENDER, NO DOCKER)

Build Command →
./build.sh

Start Command →
gunicorn threat_platform.wsgi:application

Environment Variables on Render →
SECRET_KEY
DEBUG=0
ALLOWED_HOSTS=<your-render-domain>
DATABASE_URL=<render-postgres-url>

14) DEVELOPER NOTES (EXTEND / DEBUG / MAINTAIN)
Add a New API Route →
Add serializer → monitoring/serializers.py
Add view/viewset → monitoring/views.py
Register route → monitoring/urls.py
Verify in Swagger → /api/docs/

Debugging →
Use Swagger to reproduce requests
Read terminal logs
Verify .env loads correct DATABASE_URL
Run migrations again after model changes

Future Enhancements →
Add audit logging for status changes
Add rate limiting for ingestion endpoints
Add unit tests for RBAC + alert generation
Add async workers (Celery) if events volume grows

15) CONCLUSION
This project provides a secure and scalable backend system for ingesting threat events and managing alerts using DRF best practices.

It demonstrates:
JWT authentication
Admin/Analyst RBAC
Event ingestion
Automatic alert creation
Alert filtering + pagination
Admin-only status updates
Swagger documentation
A single dashboard UI for complete demonstration