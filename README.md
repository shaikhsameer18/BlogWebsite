# Debuggers Blog

A Django blog with a from-scratch editor/diff-themed design: categories, posts, a rich-text-capable admin, and a landing page built around a "tail -f" activity log instead of a generic hero banner.

Built by [Sameer Ahmed](https://github.com/), Sufiyan Shaikh, and Tauseeb Siddiqui.

## Features

- Category-organized posts with images, served from Django's admin
- Home page with a live "console" panel of recent posts, a horizontal category tab strip, a featured-post spotlight, and a paginated post grid
- Article page with a code-editor-style line gutter and a related-posts sidebar
- Category page rendered as a directory listing
- Proper 404 handling (bad slugs return 404, not a 500) and matching 404/500 pages
- Environment-based configuration — no secrets committed, safe defaults for both local dev and production
- Production-ready out of the box: WhiteNoise for static files, `DATABASE_URL` support for Postgres, security headers gated behind `DEBUG=False`

## Tech stack

| Layer | Choice |
|---|---|
| Backend | Django 4.2 |
| Admin theme | django-material |
| Images | Pillow |
| Database | SQLite locally, Postgres in production via `dj-database-url` |
| Static files | WhiteNoise (no separate CDN/S3 required to deploy) |
| WSGI server | Gunicorn |
| Frontend | Hand-written CSS (no framework) — Space Grotesk / Newsreader / JetBrains Mono, vanilla JS for nav, scroll-reveal, and the hero console animation |

No Node/build step — the frontend is plain CSS and JS served as Django static files.

## Project structure

```
BlogWebsite/
├── mywebsite/
│   ├── manage.py
│   ├── mywebsite/          # project settings, urls, wsgi/asgi
│   ├── blogwebsite/        # the app: models, views, admin, static, fixtures
│   ├── templates/          # base + all page templates
│   └── media/               # uploaded category/post images (seed data included)
├── requirements.txt
├── Procfile                 # Heroku-style deploy (release + web)
├── render.yaml               # Render.com blueprint
└── .env.example
```

## Local setup

Requires Python 3.11+.

```bash
git clone <this-repo>
cd BlogWebsite
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit DJANGO_SECRET_KEY at minimum

cd mywebsite
python manage.py migrate
python manage.py loaddata blogwebsite/fixtures/seed_data.json   # optional: demo posts/categories
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `/admin/` to manage posts and categories.

### Environment variables

See `.env.example` for the full list. The important ones:

| Variable | Purpose | Local default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django's signing key | insecure dev fallback — **always override in production** |
| `DJANGO_DEBUG` | Debug mode / verbose errors | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames | `127.0.0.1,localhost` |
| `DATABASE_URL` | Overrides SQLite with Postgres/MySQL/etc. | unset (uses SQLite) |

## Deployment

The app is a standard Django project — deploy it anywhere that runs Python. Two paths, depending on what you want:

**Quickest path:** push to GitHub, go to [render.com](https://render.com) → New → Blueprint → point it at this repo. `render.yaml` in this repo does the rest (web service + free Postgres, secret key auto-generated). See Option A below for the full walkthrough.

### Option A — Render.com (recommended: free, Postgres included, auto-deploys from GitHub)

1. Push this repo to GitHub.
2. On [render.com](https://render.com), choose **New → Blueprint**, point it at the repo. It reads `render.yaml` and provisions the web service plus a free Postgres database automatically.
3. Render generates `DJANGO_SECRET_KEY` and wires `DATABASE_URL` for you. Nothing else is required for a first deploy.
4. After the first deploy, run once from the Render shell (or let the `release` step in `Procfile`-style platforms do it):
   ```bash
   python mywebsite/manage.py createsuperuser
   ```
5. Your site is live at `https://<service-name>.onrender.com`.

Note: Render's free web service spins down after inactivity and takes ~30s to wake on the next request. Fine for a personal blog; upgrade the plan if you need it always warm.

### Option B — PythonAnywhere (recommended if you want it always-on, zero cost, and don't need Postgres)

PythonAnywhere's free tier keeps the app running (no cold starts) and gives you a persistent filesystem, so SQLite works fine long-term.

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com), open a Bash console.
2. `git clone` this repo, then `mkvirtualenv --python=python3.11 debuggers-venv` and `pip install -r requirements.txt`.
3. In the **Web** tab, create a new web app → "Manual configuration" → Python 3.11, point the virtualenv at the one you made.
4. Set the WSGI file to import `mywebsite.wsgi` from `mywebsite/mywebsite/wsgi.py` (adjust `sys.path` to include the `mywebsite/` directory).
5. Add the environment variables from `.env.example` in the Web tab's "Environment variables" section (set `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=<yourusername>.pythonanywhere.com`).
6. Set the static/media file mappings: `/static/` → `mywebsite/staticfiles`, `/media/` → `mywebsite/media`.
7. In a console: `python manage.py migrate && python manage.py collectstatic --noinput`.
8. Reload the web app.

### Generating a secret key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Known limitations / good next steps

- User-uploaded media lives on local disk — fine for a single-instance deploy, but won't survive a redeploy on platforms with ephemeral filesystems (Render's free tier included). For that, add `django-storages` with S3/Cloudflare R2.
- No test suite yet (`blogwebsite/tests.py` is a stub) — the views are small and would benefit from a handful of response-code and 404 tests.
- No search or tagging across posts — categories are the only filter today.
- Auth (login/signup) isn't implemented; all content is managed through `/admin/`.
