# Soft for project tracking

A Django web application for tracking engineering projects across
locations, teams and team members.

## Features

- **Locations** — countries/cities where projects are carried out.
- **Teams** — groups of team members working on projects.
- **Projects** — linked to a location and a team, tracked by
  progress and payment percentage.
- **Team members** — custom user model with role, years of
  experience, license number and spoken languages; supports public
  self-registration (signup) as well as admin-side management.
- Full CRUD (create, read, update, delete) for all core entities,
  with a consistent UI (icon actions, "back to list" navigation).
- Django admin panel customized for all models, with `TeamMember`
  extending the standard Django `UserAdmin`.

## Tech stack

- Python, Django
- SQLite (development database)
- django-crispy-forms with the Bootstrap 5 template pack
- Volt Dashboard (Bootstrap 5) for styling

## Project structure

```
tracking_project/      Django project settings, root urls, WSGI/ASGI
monitor/                Main application
    models.py           Location, Team, Project, Language, TeamMember
    views.py             Class-based views (list/detail/create/update/delete)
    forms.py             TeamMemberCreationForm, ProjectForm
    admin.py             Admin site configuration
    templates/monitor/  Per-model templates (location/, team/, project/,
                        teammember/)
    templates/registration/  Login, logout, signup templates
    tests/               tests_model.py, tests_view.py, tests_admin.py
static/                 Volt Dashboard assets (css, js, img, vendor)
templates/              Shared base.html and includes (sidebar, pagination)
```

## Setup

1. Clone the repository and create a virtual environment:

   ```
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in `SECRET_KEY` and any
   other environment-specific values.

4. Apply migrations:

   ```
   python manage.py migrate
   ```

5. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```
   python manage.py runserver
   ```

7. Open `http://127.0.0.1:8000/` in your browser.

## Running tests

```
python manage.py test
```

Tests are organized by concern under `monitor/tests/`:

- `tests_model.py` — model behavior (`__str__`, slug generation,
  relations, defaults).
- `tests_view.py` — access control and CRUD flows for each view.
- `tests_admin.py` — admin panel registration and field visibility.

## Code style

The project follows flake8 with a 79-character line limit and
Conventional Commits for commit messages. Comments and docstrings
are in English.
