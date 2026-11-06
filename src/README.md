# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Staff sign-in and administrator-only activity registration management
- Public activity browsing without exposing participant details

## Getting Started

1. Install the dependencies from the repository root:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:

   ```
   uvicorn src.app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | List activities; participant details are included for staff only   |
| POST   | `/auth/login`                                                      | Sign in as a teacher                                                |
| GET    | `/auth/me`                                                         | Get the current staff session                                       |
| POST   | `/auth/logout`                                                     | End the current session                                             |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (staff only)                                     |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (staff only)                                |

## Staff Accounts

Create a teacher account from the repository root. The password is stored as a salted PBKDF2 hash in a local JSON file that is excluded from Git:

```
python src/create_teacher_account.py
```

Set `SESSION_SECRET` to a long, random value before deployment so sessions remain valid across restarts and workers. Serve the site over HTTPS and set `SESSION_HTTPS_ONLY=true` in production. The local fallback secret is generated at startup and is intended only for development.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

Activity data is stored in memory, which means registrations reset when the server restarts. Teacher credentials are stored separately in `src/teacher_accounts.json`.
