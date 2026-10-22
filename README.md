# RemoteTravels

Dynamic Flask version of the RemoteTravels website (https://www.remotetravels.co.ke).
The static HTML pages have been converted into a database driven Flask application
with an admin panel, JSON API, contact/newsletter/booking forms and a job board.

The project structure follows the [aitumik/flasky](https://github.com/aitumik/flasky)
template: application factory, blueprints, `manage.py` entry point, Alembic
migrations and a pytest suite.

## Features

- **Dynamic content** – destinations, packages, experiences, wildlife, services,
  features, testimonials, job postings and legal pages are all stored in the
  database and editable from `/admin`.
- **Admin panel** – sign in at `/auth/login` to manage destinations, packages,
  experiences, jobs, legal pages, site settings and review contact/booking/job
  inquiries.
- **Forms** – contact form, newsletter subscription, booking requests and job
  applications (with CV upload).
- **JSON API** – `/api/v1/destinations`, `/api/v1/destinations/<id>`,
  `/api/v1/packages`, `/api/v1/packages/<id>`, `/api/v1/experiences`.
- **SEO** – dynamically generated `/sitemap.xml` and `/robots.txt`, per-page
  canonical URLs, and redirects from the old `*.html` URLs.

## Project layout

```
app/
  __init__.py          application factory, context processors, CLI commands
  extensions.py        db, migrate, login_manager, mail, csrf
  models.py            SQLAlchemy models (User, Role, Destination, Package, ...)
  seed.py              starter content used by `flask init-db`
  decorators.py        permission helpers
  main/                public pages, forms, sitemap, robots, legacy redirects
  auth/                login / logout
  admin/               admin panel (CRUD + inquiries + settings)
  api/                 JSON API blueprint
  templates/           Jinja templates
  static/              css (per page + site), js, images
migrations/            Alembic migrations
tests/                 pytest suite
config.py              environment configuration
manage.py              CLI entry point
```

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.sample .env          # then edit SECRET_KEY, mail settings, etc.

flask --app manage.py init-db       # create the tables and load starter content
flask --app manage.py create-admin  # create an administrator account
flask --app manage.py run --debug      # http://127.0.0.1:5000 with auto-reload
```

`create-admin` prompts for a username, email and password interactively.

## Tests

```bash
pytest -q
```

## Database migrations

```bash
flask --app manage.py db migrate -m "describe the change"
flask --app manage.py db upgrade
```

## Deployment

**Docker**

```bash
docker compose up --build
```

**Fly.io**

```bash
fly launch --no-deploy
fly deploy
```

The `Procfile` starts `gunicorn manage:app` and runs `flask db upgrade` as a
release command. Set `FLASK_CONFIG=production`, `SECRET_KEY` and
`SQLALCHEMY_DATABASE_URI` (PostgreSQL recommended) in the environment.

## Content editing

Sign in at `/auth/login` and use the `/admin` panel. Destinations, packages and
jobs get their URL slug automatically from the title, so a destination named
"Maasai Mara Safari" is published at `/destinations/maasai-mara-safari`.
Legal pages are edited at `/admin/pages` and published under `/legal/<slug>`.
Site settings (company name, phone, email, social links, hero copy) are edited
at `/admin/settings`.
